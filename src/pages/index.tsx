import clsx from 'clsx';
import Heading from '@theme/Heading';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import styles from './index.module.css';

const themes = [
  ['第一季：从单机到平台工程', '从现代 IT 系统全景进入 DevOps、平台工程、IDP 与控制面迁移。'],
  ['第二季：单机时代', 'Linux、硬件、NUMA、CPU/GPU/DPU，基础设施从物理边界开始。'],
  ['第三季：网络时代', 'C10K、eBPF、API Gateway、Service Mesh，连接逐渐变成控制系统。'],
  ['第四季：云上帝国', '虚拟化、OpenStack、Kubernetes、云控制面，资源抽象塑造平台。'],
  ['第五季：重建信任', '身份、零信任、FinOps、供应链与治理，信任成为新的基础设施。'],
  ['第六季：算力之争', 'GPU 调度、vLLM、Ray、AI Gateway，算力从资源变成战略入口。'],
  ['第七季：稳定性战争', 'Runtime、沙箱、可观测性、OpenTelemetry，复杂度倒逼工程秩序。'],
];

const future = ['OpenClaw', 'MCP', 'RAG', 'AI Assistant', 'Agent 阅读知识库', '向量检索'];

export default function Home(): JSX.Element {
  return (
    <Layout
      title="AI Native 时代的个人技术文明知识库"
      description="《现代 IT 基础设施演进史》第一季：从单机到平台时代">
      <main className={styles.page}>
        <section className={styles.hero}>
          <div className={styles.heroText}>
            <p className={styles.kicker}>AI Native Knowledge Base</p>
            <Heading as="h1">《现代 IT 基础设施演进史》</Heading>
            <p className={styles.subtitle}>七本书：从单机到 AI Native 时代</p>
            <p className={styles.summary}>
              以 ebook 的阅读节奏，梳理现代 IT 基础设施从单机、网络、云、稳定性、信任、算力一路演进到 AI Native 的系统脉络。
            </p>
            <div className={styles.actions}>
              <Link className="button button--primary button--lg" to="/read/it-infrastructure-evolution-road">
                开始阅读
              </Link>
              <Link className="button button--secondary button--lg" to="/read/yitu-it-series/book-outline">
                查看目录
              </Link>
            </div>
          </div>
          <div className={styles.heroPanel} aria-label="知识库结构">
            <div className={styles.panelHeader}>
              <span>ebook.svc.plus</span>
              <span>Live Knowledge</span>
            </div>
            <div className={styles.panelLines}>
              <span>01 / 从单机到平台工程</span>
              <span>02 / 单机时代</span>
              <span>03 / 网络时代</span>
              <span>04 / 云上帝国</span>
              <span>05 / 重建信任</span>
              <span>06 / 算力之争</span>
              <span>07 / 稳定性战争</span>
            </div>
          </div>
        </section>
        <section className={styles.themeGrid}>
          {themes.map(([title, body]) => (
            <article className={styles.themeCard} key={title}>
              <Heading as="h2">{title}</Heading>
              <p>{body}</p>
            </article>
          ))}
        </section>
        <section className={styles.future}>
          <Heading as="h2">后续预留</Heading>
          <div className={styles.futureItems}>
            {future.map((item) => (
              <span className={clsx(styles.futurePill)} key={item}>
                {item}
              </span>
            ))}
          </div>
        </section>
      </main>
    </Layout>
  );
}
