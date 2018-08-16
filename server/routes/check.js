const router = require('express').Router();

router.get('', function(req, res){
  console.log('query string: ' + req.query.name);
  console.log('user agent: ' + req.header('User-Agent'));
  res.header('Content-Type', 'application/json; charset=utf-8');
  res.send({'query_string': req.query, 'reqest_headers': req.headers});
});

router.post('', function(req, res) {
  console.log('query string: ' + req.query.name);
  console.log('body or form: ' + JSON.stringify(req.body));
  console.log('user agent: ' + req.header('User-Agent'));
  res.header('Content-Type', 'application/json; charset=utf-8');
  res.send({'body_or_form': req.body, 'reqest_headers': req.headers});
});


module.exports = router;
