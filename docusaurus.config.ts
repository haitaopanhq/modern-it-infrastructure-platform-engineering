import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: '《现代 IT 基础设施演进史》',
  tagline: '第一季：从单机到平台时代',
  favicon: 'img/favicon.svg',
  url: 'https://ebook.svc.plus',
  baseUrl: '/',
  organizationName: 'haitaopanhq',
  projectName: 'modern-it-infrastructure-evolution',
  trailingSlash: false,
  onBrokenLinks: 'warn',
  onBrokenMarkdownLinks: 'warn',
  markdown: {
    mermaid: true,
  },
  themes: ['@docusaurus/theme-mermaid'],
  i18n: {
    defaultLocale: 'zh',
    locales: ['zh'],
  },
  presets: [
    [
      'classic',
      {
        docs: {
          path: 'docs/zh',
          routeBasePath: 'read',
          sidebarPath: './sidebars.ts',
          showLastUpdateTime: true,
          showLastUpdateAuthor: true,
          editUrl:
            'https://github.com/haitaopanhq/modern-it-infrastructure-evolution/tree/main/',
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
        sitemap: {
          changefreq: 'weekly',
          priority: 0.7,
        },
      } satisfies Preset.Options,
    ],
  ],
  plugins: [
    [
      '@easyops-cn/docusaurus-search-local',
      {
        hashed: true,
        language: ['en', 'zh'],
        indexDocs: true,
        indexBlog: false,
        docsRouteBasePath: '/read',
        highlightSearchTermsOnTargetPage: true,
      },
    ],
  ],
  themeConfig: {
    metadata: [
      {
        name: 'description',
        content:
          'AI Native 时代的个人技术文明知识库，系统梳理现代 IT 基础设施从单机、网络、云、稳定性、信任、算力到 AI Native 的演进。',
      },
      {
        name: 'keywords',
        content:
          '现代 IT 基础设施, 平台工程, AI Native, OpenClaw, MCP, RAG, Agent, Docusaurus, 技术史',
      },
    ],
    image: 'img/social-card.svg',
    colorMode: {
      defaultMode: 'dark',
      disableSwitch: false,
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: '现代 IT 基础设施演进史',
      logo: {
        alt: 'Modern IT Infrastructure Evolution',
        src: 'img/favicon.svg',
      },
      items: [
        {to: '/read/it-infrastructure-evolution-road', label: '阅读', position: 'left'},
        {to: '/read/yitu-it-series/book-outline', label: '目录', position: 'left'},
        {to: '/read/agent/mcp-acp', label: 'AI Native', position: 'left'},
        {
          href: 'https://github.com/haitaopanhq/modern-it-infrastructure-evolution',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: '核心主题',
          items: [
            {label: '单机时代', to: '/read/foundation/linux-kernel/linux-never-left'},
            {label: '网络时代', to: '/read/network/c10k-ai-fabric/c10k-to-ai-fabric'},
            {label: '云上帝国', to: '/read/cloud-platform/openstack/openstack-decline'},
            {label: 'AI Native', to: '/read/agent/mcp-acp'},
          ],
        },
        {
          title: '预留能力',
          items: [
            {label: 'OpenClaw', to: '/read/openclaw-best-practices'},
            {label: 'MCP', to: '/read/agent/mcp-acp'},
            {label: 'Agent 阅读知识库', to: '/read/agent-engineering-assistant'},
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} 现代 IT 基础设施演进史.`,
    },
    prism: {
      theme: require('prism-react-renderer').themes.github,
      darkTheme: require('prism-react-renderer').themes.dracula,
      additionalLanguages: ['bash', 'json', 'yaml', 'go', 'typescript', 'python'],
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
