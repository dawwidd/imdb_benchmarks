var redis = require("redis"), client = redis.createClient(6379,'127.0.0.1');

// Benchmark params
var data = 'O:10:"SmsRequest":5:{s:2:"id";i:550845359;s:6:"sender";s:10:"OnlineCity";s:7:"message";s:140:"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus blandit faucibus magna, vitae accumsan orci iaculis sed. Morbi cras amet.";s:10:"recipients";a:1:{i:0;i:4526159917;}s:10:"dataCoding";i:0;}';
var n = 20000;
var start;
var lastOp;

client.on("error", function (err) {
	console.log("Error " + err);
});

// When connected run each step in benchmark, and update lastOp with timings
client.on("connect", function () {
	lastOp = start = new Date();
	p1delete(function() {
		lastOp = new Date();
		p2inject(function() {
			lastOp = new Date();
			p3route(function() {
				lastOp = new Date();
				p4process(complete);
			});
		});
	});
});

// Delete all keys first
function p1delete(cb)
{
	client.del('g.queue:vu:inactive','g.connection.coolsms:vu','g.connection.coolsms:active',function(err,replies) {
		var duration = (new Date().valueOf()-lastOp.valueOf())/1000;
		console.info('Delete: %s seconds',duration);
		cb();
	});
}

// Inject the messages using a multi. 
// LPUSH takes additional params in Redis 2.2 but we don't have that always, so do it the old way
function p2inject(cb)
{
	var batch = [];
	for(var i=0;i<n;i++) {
		batch[i] = ['lpush','g.queue:vu:inactive',data];
	}
	client.multi(batch).exec(function(err,replies) {
		//redis.print(err,replies);
		var duration = (new Date().valueOf()-lastOp.valueOf())/1000;
		console.info('Inject: %s seconds',duration);
		cb();
	});
}

// Route the messages
function p3route(cb)
{
	client.lindex('g.queue:vu:inactive',-1,function(err,replies) {
		if (replies) {
			client.rpoplpush('g.queue:vu:inactive','g.connection.coolsms:vu',function() {
				p3route(cb);
			});
		} else {
			var duration = (new Date().valueOf()-lastOp.valueOf())/1000;
			console.info('Route: %s seconds',duration);
			cb();
		}
	});
}

// Process the messages in batches of 100, continuing until the list is empty
function p4process(cb)
{
	client.llen('g.connection.coolsms:vu',function (err,replies) {
		if (replies && replies>0) {
			var batch = [];
			for(var i=0;i<100;i++) {
				batch[i] = ['rpoplpush','g.connection.coolsms:vu','g.connection.coolsms:active'];
			}
			client.multi(batch).exec(function(err,replies) {
				var delbatch = [];
				replies.forEach(function(smsdata){
					delbatch.push(['del','g.connection.coolsms:active',smsdata]);
				});
				client.multi(delbatch).exec(function(err,replies) {
					p4process(cb);
				});
			});
		} else {
			var duration = (new Date().valueOf()-lastOp.valueOf())/1000;
			console.info('Process: %s seconds',duration);
			cb();
		}
	});
}

// Finally print stats and close connection
function complete()
{
	client.quit(redis.print);
	var duration = (new Date().valueOf()-start.valueOf())/1000;
	console.info('Entire benchmark took: %s seconds',duration);
	console.info('SMSes pr. second: %s',n/duration);
} 
