import express from 'express';
import cors from 'cors';

const app = express();
const server_port = 3000;
const client_port = 5173;

app.use(cors({
  origin: `http://localhost:${client_port}`,
  methods: ['GET', 'POST'],
  credentials: true,
}));

app.post('/convert-text', upload.single('file'), (req, res) => {
  // File retrieval and model execution
});

app.listen(server_port, () => {
  console.log(`Server is running on http://localhost:${server_port}`);
});
