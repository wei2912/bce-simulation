(function() {
  "use strict";

  /** Load Node.js modules */
  var fs = require('fs'),
      path = require('path'),
      parseURL = require('url').parse,
      exec = require('child_process').exec,
      http = require('http');

  /** Load other modules */
  var send = require('send');

  /** Used as the port number to run a server on */
  var port = +process.env.PORT || 8080;

  var root = path.join(__dirname, 'public');

  function reqListener(req, res) {
    console.log(req.url);
    var url = parseURL(req.url, true);

    if (url.pathname == '/build' && url.query) {
      return build(req, res, url.query);
    }

    send(req, url.pathname, {root: root})
      .on('error', error)
      .on('directory', redirect)
      .pipe(res);

    function error(err) {
      res.statusCode = err.status || 500;
      res.end(err.message);
    }

    function redirect() {
      res.statusCode = 301;
      res.setHeader('Location', req.url + '/');
      res.end('Redirecting to ' + req.url + '/');
    }
  }

  function build(req, res, query) {
    var type = query.simulation;
    if (!/^(?:coin(?:_phy)?|needle)$/.test(type)) {
      res.end("unsupported");
    }

    var mode = query['type'],
        trials = query.trials,
        step = query.step,
        isCoin = /^coin/.test(type),
        // Coin experiments
        radius = query.radius,
        width = query.width,
        // Needle experiments
        length = query.length,
        gap = query.gap;

    var fileName = path.join(
      __dirname,
      'output/' + type + '.' + mode + '.' + trials + '.' + step + '.' +
      (isCoin ? radius + '.' + width : length + '.' + gap) +
      '.png'
    );
    var fileToExec = path.join(__dirname, type + '_graph.py');
    var args = ['python', fileToExec, '-o', fileName, '-m', mode, '-t', trials, '-s', step];
    if (isCoin) {
      args.push('-r', radius, '-g', width);
    } else {
      args.push('-l', length, '-g', gap);
    }
    console.log(args = args.join(' '));
    exec(args, function(err, stderr, stdout) {
      if (err || stderr) {
        return res.end((err || stderr).toString());
      }
      res.setHeader('content-type', 'image/png');
      fs.createReadStream(fileName).pipe(res).on('finish', function() {
        fs.unlink(fileName, function(err) {
          if (err) {
            console.error(err);
          }
        });
      });
    });
  }

  http.createServer(reqListener).listen(port, function() {
    console.log('Listening on port ' + port);
  });

}.call(this));
