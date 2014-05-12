(function() {
  "use strict";

  /** Load Node.js modules */
  var fs = require('fs'),
      path = require('path'),
      parseURL = require('url').parse,
      spawn = require('child_process').spawn,
      http = require('http');

  /** Load other modules */
  var send = require('send');

  /** Used as the port number to run a server on */
  var port = +process.env.PORT || 8080;

  var root = path.join(__dirname, 'public');

  var executable = process.platform == 'win32' ? path.normalize('C:\\Python27\\python.exe') : 'python';

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
      'output' + type + '.' + query.trials + '.' + query.gap + '.'
      + (type == 'coin' ? query.radius : query.length) + '.' + query.step + '.png'
    );
    var fileToExec = path.join(__dirname, type + '-graph.py');
    var args = ['-o', fileName, '-t', query.trials, '-g', query.gap, '-s', query.step];
    args.push(type == 'coin' ? '-r' : '-l', type == 'coin' ? query.radius : query.length);
    args.unshift(fileToExec);
    console.log(args);
    spawn(executable, args, function(err) {
      if (err) {
        return res.end(err + '');
      }
      res.setHeader('content-type', 'image/png');
      fs.createReadStream(fileName).pipe(res).on('finish', function() {
        fs.unlink(fileName, function(){})
      });
    });
  }

  http.createServer(reqListener).listen(port, function() {
    console.log('Listening on port ' + port);
  });

}.call(this));
