(function() {
  "use strict";

  /** Load Node.js modules */
  var fs = require('fs'),
      path = require('path'),
      parseURL = require('url').parse,
      exec = require('child_process').exec;

  /** Load other modules */
  var send = require('send');

  /** Used as the port number to run a server on */
  var port = +process.env.PORT || 8080;

  var root = path.join(__dirname, 'public');

  var outputFolder = path.join(__dirname, 'output');

  if (fs.existsSync(outputFolder)) {
    fs.rmdirSync(outputFolder);
  }

  fs.mkdirSync(outputFolder);

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
    if (!/^(?:coin(?:_phy)?|needle|all)$/.test(type)) {
      res.end("unsupported");
    }

    var mode = query['type'],
        trials = query.trials,
        step = query.step,
        isCoin = /^coin/.test(type),
        isAll = /^all$/.test(type),
        // Coin experiments
        diameter = query.diameter,
        width = query.width,
        // Needle experiments
        length = query.length,
        gap = query.gap;

    var fileName = path.join(
      __dirname,
      'output/' + type + '.' + mode + '.' + trials + '.' + step + '.' +
      (isCoin ? diameter + '.' + width : isAll ? diameter + '.' + width : length + '.' + gap) +
      '.png'
    );
    var fileToExec = path.join(__dirname, type + '.py');
    var args = ['python', fileToExec, 'plot', '-o', fileName, '-m', mode];
    if (!isAll) {
      args.push('-t', trials, '-s', step);
    }
    if (isCoin || isAll) {
      args.push(isAll ? '-l' : '-d', diameter, '-g', width);
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

  if (!module.parent) {
    require('http').createServer(reqListener).listen(port, function() {
      console.log('Listening on port ' + port);
    });
  } else {
    module.exports = reqListener;
  }

}.call(this));
