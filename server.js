"use strict";

/** Load Node.js modules */
var fs = require('fs'),
    path = require('path'),
    exec = require('child_process').exec;

/** Load other modules */
var Hapi = require('hapi');

/** Used as the port number to run a server on */
var port = +process.env.PORT || 8080;

var outputFolder = path.join(__dirname, 'output');

if (fs.existsSync(outputFolder)) {
  fs.rmdirSync(outputFolder);
}

fs.mkdirSync(outputFolder);

var resultsFile = fs.readFileSync(path.join(__dirname, 'public/results.html'), 'utf8');

// Create a server with a host and port
var server = new Hapi.Server({
  connections: {
    routes: {
      files: {
        relativeTo: __dirname
      }
    }
  }
});

server.connection({
  port: port
});

server.route({
  method: 'GET',
  path: '/api',
  handler: api
});

server.route({
  method: 'GET',
  path: '/build.png',
  handler: build
});

server.route({
  method: 'GET',
  path: '/{param*}',
    handler: {
    directory: {
      path: 'public'
    }
  }
});

function api(request, reply) {
  var query = request.query;
  
  var problem = query.problem;
  if (!/^(?:coin|needle)(?:_var)?$/.test(problem)) {
    reply("Unsupported");
  }
  var length = query.length,
      gap = query.gap,
      trials = query.trials;

  var args = ['python', 'buffon.py', 'run', problem, length, gap, '--trials', trials];
  console.log(args = args.join(' '));

  exec(args, function(err, stderr, stdout) {
    if (err || stderr) {
      return reply(resultsFile.replace('{{results}}', (err || stderr).toString().replace('\n', '<br>')));
    }
    reply(resultsFile.replace('{{results}}', stdout.replace('\n', '<br>')));
  });
}

function build(request, reply) {
  var query = request.query;

  var type = query.simulation;
  if (!/^(?:length|gap_width)$/.test(type)) {
    reply("Unsupported");
  }

  var xmin = query.xmin,
      xmax = query.xmax;

  var fileName = path.join(
    __dirname,
    'output/' +
    type + '.' +
    xmin + '.' +
    xmax + '.' +
    'png'
  );

  var args = ['python', 'buffon.py', 'plot', type, /* xmin */ xmin, /* xmax */ xmax, '--output', fileName];
  console.log(args = args.join(' '));

  exec(args, function(err, stderr, stdout) {
    if (err || stderr) {
      return reply((err || stderr).toString());
    }
    reply
      .file(fileName)
      .type('image/png')
      .once('finish', function() {
        fs.unlink(fileName, function(err) {
          if (err) {
            console.error(err);
          }
        });
      });
  });
}

if (!module.parent) {
  process.env.SERVER = true;
  server.start();
} else {
  module.exports = server;
}
