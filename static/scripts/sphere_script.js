var scene = {
	sphereRadius: 250,
	dots: 800,
	dotSize: 1.2,
	speed: 3,
	inclination: -0,
	zDist: 700,
	focal: 600
};

var c = document.getElementById('c'),
	ctx = c.getContext('2d');

function resize()
{
	c.width = c.offsetWidth;
	c.height = c.offsetHeight;
	ctx.fillStyle = '#aaaaa';
	ctx.globalCompositeOperation = 'lighter';
}
window.addEventListener('resize', resize);
resize();

var angleOffset = 0;
var angleOffsetGoal = 0;
c.addEventListener('mousemove', function(e) { angleOffsetGoal = Math.PI * (e.clientX / c.width - .5); });

var baseDots = [];
// Creating points on the sphere (used http://www.mcadcentral.com/solidworks-modeling/25421-even-distributi-n-points-n-sphere.html#post121272)
(function()
{
	var inc = Math.PI * (3 - Math.sqrt(5));
	var off = 2 / scene.dots;
	for(var i = 0; i < scene.dots; i++)
	{
		var y = (i + .5) * off - 1;
		var r = Math.sqrt(1 - y*y);
		var phi = i * inc;
		baseDots.push([
			scene.sphereRadius * r * Math.cos(phi),
			scene.sphereRadius * y,
			scene.sphereRadius * r * Math.sin(phi)
		]);
	}
})();

function dup(p) { return [p[0], p[1], p[2]]; }
function rotateX(p, a)
{
	var d = Math.sqrt(p[2] * p[2] + p[1] * p[1]),
		na = Math.atan2(p[1], p[2]) + a;
	return [p[0], d * Math.sin(na), d * Math.cos(na)];
}
function rotateY(p, a)
{
	var d = Math.sqrt(p[2] * p[2] + p[0] * p[0]),
		na = Math.atan2(p[2], p[0]) + a;
	return [d * Math.cos(na), p[1], d * Math.sin(na)];
}
function projection(p, focal) { return [focal * p[0] / p[2], focal * p[1] / p[2], p[2]]; }

function loop()
{
	requestAnimationFrame(loop);
	angleOffset += (angleOffsetGoal - angleOffset) * .1;
	ctx.clearRect(0,0,c.width,c.height);
	var m = [c.width *.5, c.height * .5];
	var time = Date.now() * 0.001 * scene.speed;
	var offset = scene.sphereRadius * (Math.sin(time) + 1);
	ctx.beginPath();
	for(var i = 0, l = baseDots.length; i < l; i++)
	{
		var p = dup(baseDots[i]);
		p[1] += offset;
		if(p[1] > scene.sphereRadius) p[1] = scene.sphereRadius;
		p = rotateX(rotateY(p, angleOffset), scene.inclination);
		p[2] += scene.zDist;
		var size = scene.focal * scene.dotSize / p[2];
		p = projection(p, scene.focal);
		ctx.moveTo(m[0] + p[0], m[1] + p[1]);
		ctx.arc(m[0] + p[0], m[1] + p[1], size, 0, 2 * Math.PI);
	}
	ctx.fill();
}
requestAnimationFrame(loop);