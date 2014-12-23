var http = require('http'),
    path = require('path'),
    fs = require('fs');

var lab = exports.lab = require('lab').script(),
    assert = require('assert');

var describe = lab.experiment,
    it = lab.test,
    before = lab.before,
    after = lab.after;

var server = require('../server');

describe('server', function () {
  var contentTypes = {
    'text': /^text\/plain(?:; charset=.+)?$/,
    'html': /^text\/html(?:; charset=.+)?$/,
    'css': /^text\/css(?:; charset=.+)?$/
  };

  var files = [{
    'name': 'index.html',
    'type': contentTypes.html
  }, {
    'name': 'css/normalize.css',
    'type': contentTypes.css
  }, {
    'name': 'css/main.css',
    'type': contentTypes.css
  }].map(function (file) {
    file.contents = fs.readFileSync(path.join(__dirname, '../public', file.name), 'utf-8');
    return file;
  });

  files.forEach(function (file) {
    var name = file.name;
    it('should return correct files for `' + name + '`', function (done) {
      server.inject('/' + name, function (res) {
        assert.equal(res.statusCode, 200, 'Status code');
        assert(file.type.test(res.headers['content-type']), 'File type');
        assert.equal(file.contents, res.rawPayload.toString('utf8'), 'File contents');
        done();
      });
    });
  });
});
