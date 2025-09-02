# Deploy HTML Wrapper to Render.com

## 🚀 **Super Easy Deployment**

This HTML wrapper gives you **true iPhone app experience** with:
- ✅ No URL bar when added to Home Screen
- ✅ Full-screen display
- ✅ Native app-like interface
- ✅ Proper meta tags for iOS

## 📱 **How to Deploy**

### **Step 1: Update the iframe URL**
In `index.html`, change this line:
```html
src="https://your-streamlit-app.onrender.com"
```
To your actual Streamlit app URL on Render.com

### **Step 2: Deploy to Render.com**
1. **Go to [Render.com](https://render.com)**
2. **Click "New +"** → **"Static Site"**
3. **Connect your GitHub repo** or upload files
4. **Configure:**
   - **Name**: `equity-dashboard-html`
   - **Build Command**: (leave empty - not needed for static HTML)
   - **Publish Directory**: (leave empty - not needed)
5. **Click "Create Static Site"**

### **Step 3: Add to iPhone Home Screen**
1. **Open your deployed HTML app** in Safari
2. **Tap the Share button** (square with arrow)
3. **Tap "Add to Home Screen"**
4. **Customize the name** if you want
5. **Tap "Add"**

## 🎯 **Result**
- **App icon** appears on your Home Screen
- **Taps open in full-screen** (no URL bar!)
- **Looks and feels** like a native app
- **Your Streamlit dashboard** runs inside the wrapper

## ⚡ **Why This Works Better**
- **HTML wrapper** has proper meta tags
- **Streamlit runs** in iframe (no limitations)
- **Render.com** serves static HTML perfectly
- **iOS Safari** recognizes it as a web app

## 🔧 **Customization**
- Change colors in the CSS
- Modify the header text
- Adjust the iframe source URL
- Add your own app icon

**Much simpler than Streamlit deployment and gives you the iPhone app experience you want!**
