import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const config: Config = {
  title: 'DES3D User Manual',
  tagline: 'Essential information for using DES3D',
  favicon: 'img/favicon.png',

  // Set the production url of your site here
  url: 'https://geoflac.github.io',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/des3d/',
  projectName: 'geoflac.github.io',
  organizationName: 'geoflac',
  trailingSlash: false,

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  // organizationName: 'https://geoflac.github.io/', // Usually your GitHub org/user name.
  // projectName: 'des3d/', // Usually your repo name.
  organizationName: 'geoflac', // Usually your GitHub org/user name.
  projectName: 'des3d', // Usually your repo name.
  deploymentBranch: 'main',

  onBrokenLinks: 'ignore', //throw',
  onBrokenMarkdownLinks: 'warn',

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
        {
          type: 'docSidebar',
          sidebarId: 'usermanualSidebar',
          position: 'left',
          label: 'User Manual',
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
          title: 'DES3D Documentation',
          items: [
            {
              label: 'Introduction',
              to: '/docs/intro',
            },
            {
              label: 'Usage',
              to: '/docs/usage',
            },
            {
              label: 'Tutorial',
              to: '/docs/tutorial',
            },
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
              label: 'DES3D on GitHub',
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
    <img src="@site/static/img/nsf-logo.png" alt="NSF Logo" style="height:40px; margin-top:8px;"/>
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
  }, // satisfies Preset.ThemeConfig,
};

export default config;
