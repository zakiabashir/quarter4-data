const { themes } = require('prism-react-renderer');
const lightCodeTheme = themes.github;
const darkCodeTheme = themes.dracula;

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'AI-Native Physical AI Textbook',
  tagline: 'A comprehensive guide to Physical AI and Humanoid Robotics',
  favicon: 'img/favicon.ico',

  url: 'https://ai-textbook.example.com',
  baseUrl: '/',

  organizationName: 'ai-textbook',
  projectName: 'physical-ai-textbook',

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          editUrl: 'https://github.com/ai-textbook/physical-ai-textbook/tree/main/',
        },
        blog: false,
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      },
    ],
  ],

  themeConfig: {
    navbar: {
      title: 'Physical AI Textbook',
      logo: {
        alt: 'Physical AI Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: 'Chapters',
        },
        {
          href: 'https://github.com/ai-textbook/physical-ai-textbook',
          label: 'GitHub',
          position: 'right',
        },
        {
          to: '/chat',
          label: 'AI Assistant',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Resources',
          items: [
            {
              label: 'Documentation',
              to: '/docs/intro',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} AI-Native Physical AI Textbook.`,
    },
    prism: {
      theme: lightCodeTheme,
      darkTheme: darkCodeTheme,
      additionalLanguages: ['python', 'cpp', 'yaml', 'json', 'bash'],
    },
  },

  plugins: [
    [
      '@docusaurus/plugin-content-docs',
      {
        id: 'chat',
        path: 'chat',
        routeBasePath: 'chat',
        sidebarPath: false,
      },
    ],
  ],
};

module.exports = config;