# Smart Parking System - Railway Deployment Guide

## Prerequisites
- GitHub account
- Railway account (sign up at [railway.app](https://railway.app))
- Git installed on your computer

## Deployment Steps

### 1. Prepare Your Repository
```bash
# Initialize git repository (if not already done)
git init

# Add all files
git add .

# Commit changes
git commit -m "Initial commit for Railway deployment"

# Create a new repository on GitHub and push
git remote add origin https://github.com/yourusername/smart-parking.git
git branch -M main
git push -u origin main
```

### 2. Deploy to Railway

#### Option A: Deploy from GitHub (Recommended)
1. Go to [railway.app](https://railway.app) and sign in
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your smart-parking repository
5. Railway will automatically detect the Python project and start building

#### Option B: Deploy using Railway CLI
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Initialize project
railway init

# Deploy
railway up
```

### 3. Configure Environment (if needed)
Railway automatically detects most configurations, but you can add environment variables if needed:
- Go to your project dashboard
- Click on "Variables" tab
- Add any custom environment variables

### 4. Monitor Deployment
- Check the "Deployments" tab for build logs
- Once deployed, Railway will provide a public URL
- Your app will be available at: `https://your-app-name.railway.app`

## File Structure for Deployment
```
Smart Parking/
├── main.py                 # Main Flask application
├── requirements.txt        # Python dependencies
├── Procfile               # Process file for Railway
├── railway.json           # Railway configuration
├── .gitignore            # Git ignore file
├── model_final.h5        # Trained model
├── carposition.pkl       # Parking positions
├── car_test.mp4         # Test video
├── templates/
│   └── index.html       # Frontend template
└── train_data/          # Training data (optional for deployment)
```

## Important Notes

### File Size Considerations
- Railway has size limits for deployments
- Consider uploading large files (video, model) to cloud storage if deployment fails
- For production, consider using:
  - AWS S3 for video files
  - Google Cloud Storage for model files

### Performance Optimizations
- The app is configured with single worker to handle video processing
- Memory usage is optimized for Railway's free tier
- Real-time video streaming may require upgrading to a paid plan for better performance

### Troubleshooting

#### Common Issues:
1. **Build fails due to OpenCV**: Uses `opencv-python-headless` for server compatibility
2. **Memory issues**: Railway free tier has 512MB RAM limit
3. **Model loading errors**: Ensure all pickle and model files are included in repository

#### Solutions:
- Check Railway logs in the dashboard
- Monitor memory usage in Railway metrics
- For large models, consider model compression or cloud storage

### Alternative Video Sources
For production deployment, consider:
- Live camera feeds via RTSP URLs
- Cloud-hosted video files
- User-uploaded videos through web interface

## Post-Deployment
1. Test all endpoints:
   - `/` - Main dashboard
   - `/video_feed` - Video stream
   - `/space_count` - API endpoint

2. Monitor performance in Railway dashboard
3. Set up custom domain (optional)
4. Configure scaling if needed

## Cost Considerations
- Railway free tier: 512MB RAM, $5 credit/month
- For production use: Consider upgrading to hobby plan ($5/month)
- Video processing is memory-intensive, monitor usage

## Security Notes
- App runs in production mode with debug disabled
- Consider adding authentication for production use
- Environment variables are secure in Railway

## Support
- Railway Documentation: [docs.railway.app](https://docs.railway.app)
- Railway Discord: [railway.app/discord](https://railway.app/discord)
- GitHub Issues: Create issues in your repository for project-specific problems
