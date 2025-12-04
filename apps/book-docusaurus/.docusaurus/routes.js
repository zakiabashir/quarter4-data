import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/__docusaurus/debug',
    component: ComponentCreator('/__docusaurus/debug', '5ff'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/config',
    component: ComponentCreator('/__docusaurus/debug/config', '5ba'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/content',
    component: ComponentCreator('/__docusaurus/debug/content', 'a2b'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/globalData',
    component: ComponentCreator('/__docusaurus/debug/globalData', 'c3c'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/metadata',
    component: ComponentCreator('/__docusaurus/debug/metadata', '156'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/registry',
    component: ComponentCreator('/__docusaurus/debug/registry', '88c'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/routes',
    component: ComponentCreator('/__docusaurus/debug/routes', '000'),
    exact: true
  },
  {
    path: '/chat',
    component: ComponentCreator('/chat', '10e'),
    routes: [
      {
        path: '/chat',
        component: ComponentCreator('/chat', 'e6f'),
        routes: [
          {
            path: '/chat',
            component: ComponentCreator('/chat', 'e9f'),
            routes: [
              {
                path: '/chat/intro',
                component: ComponentCreator('/chat/intro', '144'),
                exact: true
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '/docs',
    component: ComponentCreator('/docs', '296'),
    routes: [
      {
        path: '/docs',
        component: ComponentCreator('/docs', 'cc9'),
        routes: [
          {
            path: '/docs',
            component: ComponentCreator('/docs', '60f'),
            routes: [
              {
                path: '/docs/chapter1/introduction',
                component: ComponentCreator('/docs/chapter1/introduction', '77a'),
                exact: true
              },
              {
                path: '/docs/chapter1/sensors-and-perception',
                component: ComponentCreator('/docs/chapter1/sensors-and-perception', '053'),
                exact: true
              },
              {
                path: '/docs/chapter2/introduction',
                component: ComponentCreator('/docs/chapter2/introduction', '6f3'),
                exact: true
              },
              {
                path: '/docs/intro',
                component: ComponentCreator('/docs/intro', '61d'),
                exact: true,
                sidebar: "tutorialSidebar"
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
