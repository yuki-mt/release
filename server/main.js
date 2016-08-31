const jsonServer = require('json-server');
const app = jsonServer.create();
const jsonRouter = jsonServer.router('db.json');
const checkRouter = require('./routes/check');
const middlewares = jsonServer.defaults();
const port = process.env.PORT || 3000;
const bodyParser = require('body-parser');

app.use(bodyParser.urlencoded({extended: true}));
app.use(bodyParser.json());

app.use(middlewares);
app.use('/json', jsonRouter);
app.use('/check', checkRouter);


app.listen(port);
