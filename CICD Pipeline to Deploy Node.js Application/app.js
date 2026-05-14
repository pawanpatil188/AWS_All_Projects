const http = require('http');

const PORT = process.env.PORT || 3000;

const server = http.createServer((req, res) => {
    res.writeHead(200, { 'Content-Type': 'text/html' });
    res.end(`
        <h1>🚀 CI/CD Pipeline Deployed Successfully!</h1>
        <p>This Node.js app is running via automated AWS pipeline.</p>
    `);
});

server.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});