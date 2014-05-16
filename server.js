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
    var type = query.type;
    if (!/^(?:coin|needle(?:-angle)?)$/.test(type)) {
      res.end("unsupported");
    }
    var fileName = path.join(
      __dirname,
      'output/' + type + '.' + query.trials + '.' + query.gap + '.'
      + (type == 'coin' ? query.radius : query.length) + '.' + query.step + '.png'
    );
    var fileToExec = path.join(__dirname, type + '-graph.py');
    var args = ['python', fileToExec, '-o', fileName, '-t', query.trials, '-g', query.gap, '-s', query.step];
    args.push(type == 'coin' ? '-r' : '-l', type == 'coin' ? query.radius : query.length);
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
