export default async function handler(req, res) {
    if (req.method !== 'POST') {
      return res.status(405).json({ message: 'Method not allowed' });
    }
  
    try {
      const { topic } = req.body;
      const response = await fetch('http://localhost:8000/generate-video', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ topic }),
      });
  
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || 'Backend error');
      res.status(200).json(data);
    } catch (error) {
      res.status(500).json({ message: error.message });
    }
  }