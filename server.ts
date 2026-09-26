import express, { Request, Response } from 'express';
import { createServer as createViteServer } from 'vite';
import path from 'path';
import { fileURLToPath } from 'url';
import { dataService } from './src/server/dataService.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

async function startServer() {
  const app = express();
  const PORT = Number(process.env.PORT) || 3000;

  app.use(express.json());

  // API Routes
  app.get('/api/overview', (req: Request, res: Response) => {
    try {
      const overview = dataService.getOverview();
      res.json(overview);
    } catch (err) {
      console.error('Error fetching overview:', err);
      res.status(500).json({ error: 'Failed to fetch overview data' });
    }
  });

  app.get('/api/customers', (req: Request, res: Response) => {
    try {
      const params = {
        search: req.query.search as string,
        risk_category: req.query.risk_category as string,
        predicted_churn: req.query.predicted_churn as string,
        contract: req.query.contract as string,
        internet_service: req.query.internet_service as string,
        payment_method: req.query.payment_method as string,
        sort_by: req.query.sort_by as any,
        sort_order: req.query.sort_order as any,
        page: req.query.page ? parseInt(req.query.page as string, 10) : 1,
        limit: req.query.limit ? parseInt(req.query.limit as string, 10) : 20,
      };

      const result = dataService.getCustomers(params);
      res.json(result);
    } catch (err) {
      console.error('Error fetching customers:', err);
      res.status(500).json({ error: 'Failed to fetch customer list' });
    }
  });

  app.get('/api/customers/:id', (req: Request, res: Response) => {
    try {
      const customerID = req.params.id;
      const customer = dataService.getCustomerById(customerID);
      if (!customer) {
        return res.status(404).json({ error: `Customer ID '${customerID}' not found` });
      }
      res.json(customer);
    } catch (err) {
      console.error('Error fetching customer detail:', err);
      res.status(500).json({ error: 'Failed to fetch customer detail' });
    }
  });

  app.get('/api/risk-analysis', (req: Request, res: Response) => {
    try {
      const analysis = dataService.getRiskAnalysis();
      res.json(analysis);
    } catch (err) {
      console.error('Error fetching risk analysis:', err);
      res.status(500).json({ error: 'Failed to fetch risk analysis' });
    }
  });

  app.get('/api/model-insights', (req: Request, res: Response) => {
    try {
      const insights = dataService.getModelInsights();
      res.json(insights);
    } catch (err) {
      console.error('Error fetching model insights:', err);
      res.status(500).json({ error: 'Failed to fetch model insights' });
    }
  });

  // Vite development middleware or production static server
  if (process.env.NODE_ENV !== 'production') {
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: 'spa',
    });
    app.use(vite.middlewares);
  } else {
    app.use(express.static(path.join(__dirname, 'dist')));
    app.get('*', (req: Request, res: Response) => {
      res.sendFile(path.join(__dirname, 'dist', 'index.html'));
    });
  }

  app.listen(PORT, '0.0.0.0', () => {
    console.log(`[Churn Intelligence] Server running on http://0.0.0.0:${PORT}`);
  });
}

startServer().catch((err) => {
  console.error('Failed to start server:', err);
  process.exit(1);
});
