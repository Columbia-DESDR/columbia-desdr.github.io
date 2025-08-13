# DESDR Main Website

A React-based website for the Data for Evidence-based Solutions for Development and Resilience (DESDR) project at Columbia University.

## Quick Start

```bash
# Install dependencies
npm install

# Start development server
npm start

# Build and deploy to GitHub Pages
npm run deploy
```

## Project Structure

```
src/
├── pages/           # Main page components
│   ├── Home.js      # Landing page
│   ├── SurveyYourWay.js
│   ├── Reptile.js
│   └── Sliders.js
├── components/      # Reusable components
├── constants.js     # Configuration (countries, links, etc.)
└── images/         # Images and static files
```

## Making Changes

### Adding Countries to Sliders

Edit `src/constants.js` in the `toolkit` array, specifically the Sliders section:

```javascript
{name: '03. Sliders →', deployed: [
  // Add new countries here:
  {name: 'CountryName →', link: 'https://columbia-desdr.github.io/Sliders-countryname/config'}
]}
```

### Updating Content

- **Page content**: Edit files in `src/pages/`
- **Links and data**: Modify `src/constants.js`
- **Styling**: Update CSS files in respective components

## Development Workflow

1. **Local Development**
   ```bash
   npm start
   ```
   - Opens `http://localhost:3000`
   - Auto-reloads on changes

2. **Testing Changes**
   - Verify all links work
   - Check responsive design
   - Test navigation

3. **Deployment**
   ```bash
   npm run deploy
   ```
   - Builds production version
   - Deploys to GitHub Pages
   - Site updates at `https://columbia-desdr.github.io`

## Important Notes

- **GitHub Pages**: Site auto-deploys from `gh-pages` branch
- **Country URLs**: Follow pattern `Sliders-countryname` for consistency
- **Testing Required**: Always test locally before deploying
- **Assets**: Place images in `src/images/`

## Technology Stack

- React 18
- React Router (navigation)
- GitHub Pages (hosting)
- Node.js/npm (build tools)

## Troubleshooting

- **Deploy fails**: Check GitHub Pages settings
- **Links broken**: Verify target URLs exist
- **Build errors**: Run `npm install` and check console

## Contact

For questions about the DESDR project, contact the Columbia University IRI team.