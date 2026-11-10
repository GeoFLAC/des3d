import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

// Maintainer sync record: general baseline DynEarthSol #114 (2026-10-31);
// PT mechanics #106 and build requirements #122/#125 are also documented.
// RSF theory and tutorials cover #91; tutorial figures come from master 68cc2a0.


// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const config: Config = {
  title: 'DynEarthSol Documentation',
  tagline: 'Using DynEarthSol (DES2D and DES3D) for geodynamics, earthquake cycles and surface processes',
  favicon: 'img/favicon.png',

  // Set the production url of your site here
  url: 'https://geoflac.github.io',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/des3d/',
  trailingSlash: false,

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'geoflac', // Usually your GitHub org/user name.
  projectName: 'des3d', // Usually your repo name.
  deploymentBranch: 'main',

  onBrokenLinks: 'throw',
  onBrokenAnchors: 'throw',
  markdown: {
    hooks: {
      onBrokenMarkdownLinks: 'throw',
    },
  },

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          remarkPlugins: [remarkMath],
          rehypePlugins: [[rehypeKatex, {output: 'html'}]],
          lastVersion: 'current',
          versions: {
            current: {
              label: 'Latest',
              path: '',
            },
          },
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          // editUrl:
          //   'https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/',
        },
        blog: {
          showReadingTime: true,
          feedOptions: {
            type: ['rss', 'atom'],
            xslt: true,
          },
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          // editUrl:
          //   'https://github.com/GeoFLAC/des3d/',
          // Useful options to enforce blogging best practices
          onInlineTags: 'warn',
          onInlineAuthors: 'warn',
          onUntruncatedBlogPosts: 'warn',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  plugins: [
    [
      '@docusaurus/plugin-client-redirects',
      {
        // Category pages renamed in the 2026 reorganization.
        redirects: [
          {from: '/docs/category/usage', to: '/docs/category/user-guide'},
          {from: '/docs/category/tutorials', to: '/docs/category/fundamental-mechanics'},
        ],
      },
    ],
  ],

  themes: [
    [
      require.resolve('@easyops-cn/docusaurus-search-local'),
      {
        hashed: true,
        language: ['en'],
        indexDocs: true,
        indexPages: false,
        docsRouteBasePath: '/docs',
      },
    ],
  ],

  themeConfig: {
    // Replace with your project's social card
    image: 'img/docusaurus-social-card.jpg',
    navbar: {
      title: 'Main',
      logo: {
        alt: 'GeoFLAC Logo',
        src: 'img/logo.svg',
      },
      items: [
        {to: '/docs/intro', position: 'left', label: 'Overview'},
        {to: '/docs/category/getting-started', position: 'left', label: 'Getting started'},
        {to: '/docs/category/user-guide', position: 'left', label: 'User guide'},
        {to: '/docs/category/tutorial', position: 'left', label: 'Tutorials'},
        {to: '/docs/category/theory', position: 'left', label: 'Theory'},
        {to: '/docs/category/reference', position: 'left', label: 'Reference'},
        {
          type: 'docsVersionDropdown',
          position: 'right',
        },
        // {to: '/blog', label: 'Blog', position: 'left'},
        // {
        //   href: 'https://github.com/facebook/docusaurus',
        //   label: 'GitHub',
        //   position: 'right',
        // },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Documentation',
          items: [
            {label: 'Overview', to: '/docs/intro'},
            {label: 'Getting started', to: '/docs/category/getting-started'},
            {label: 'User guide', to: '/docs/category/user-guide'},
            {label: 'Tutorials', to: '/docs/category/tutorial'},
            {label: 'Theory', to: '/docs/category/theory'},
            {label: 'Reference', to: '/docs/category/reference'},
          ],
        },
        {
          title: 'Community',
          items: [
            {
              label: 'GeoFLAC on GitHub',
              href: 'https://github.com/GeoFLAC/',
            },
          ],
        },
        {
          title: 'More',
          items: [
            // {
            //   label: 'Blog',
            //   to: '/blog',
            // },
            {
              label: 'DynEarthSol on GitHub',
              href: 'https://github.com/GeoFLAC/DynEarthSol/',
            },
            {
              label: 'LAGHOST on GitHub',
              href: 'https://github.com/GeoFLAC/Laghost/',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Team GeoFLAC. Built with Docusaurus. Supported by the National Science Foundation Award 2104002.
  <br/>
  <a href="https://www.nsf.gov/" target="_blank" rel="noopener noreferrer">
    <img src="/des3d/img/nsf-logo.png" alt="NSF Logo" style="height:40px; margin-top:8px;"/>
  </a>`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },

    // stylesheets: [
    //   {
    //     href: 'https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css', // Example CDN URL for a recent KaTeX
    //     type: 'text/css',
    //   },
    // ],
  } satisfies Preset.ThemeConfig,
};

export default config;
