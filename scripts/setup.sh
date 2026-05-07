#!/bin/bash
set -e

echo "🚀 AI SaaS Kit — Setup"
echo ""

# Check for Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is required. Please install Node.js 18+ first."
    exit 1
fi

echo "📦 Installing dependencies..."
npm install

echo ""
echo "🔧 Setting up environment..."
if [ ! -f .env.local ]; then
    cp .env.example .env.local
    echo "✅ Created .env.local — please fill in your API keys"
else
    echo "⚠️  .env.local already exists, skipping"
fi

echo ""
echo "🗄️  Setting up database..."
npx prisma generate
npx prisma db push

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Fill in your API keys in .env.local"
echo "  2. Run 'npm run dev' to start the development server"
echo "  3. Open http://localhost:3000"
echo ""
echo "Happy building! 🎉"
