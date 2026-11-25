import {useState, type ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useBaseUrl from '@docusaurus/useBaseUrl';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';
import CodeBlock from '@theme/CodeBlock';
import HomepageFeatures from '@site/src/components/HomepageFeatures';

import styles from './index.module.css';

const TAGLINE =
  'Dynamic Earth Solver: an explicit Lagrangian finite element code for ' +
  'tectonics, earthquake cycles and surface processes on unstructured ' +
  '2D and 3D meshes.';

function HomepageHeader() {
  const banner = useBaseUrl('/img/banner.png');
  return (
    <header
      className={clsx('hero hero--dark', styles.heroBanner)}
      style={{backgroundImage: `url(${banner})`}}>
      <div className={clsx('container', styles.heroContent)}>
        <Heading as="h1" className="hero__title">
          DynEarthSol
        </Heading>
        <p className="hero__subtitle">{TAGLINE}</p>
        <div className={styles.buttons}>
          <Link className="button button--primary button--lg" to="#quick-start">
            Quick start
          </Link>
          <Link className="button button--secondary button--lg" to="/docs/intro">
            User manual
          </Link>
        </div>
      </div>
    </header>
  );
}

type Highlight = {title: string; text: string};

const Highlights: Highlight[] = [
  {
    title: 'Explicit dynamic relaxation',
    text:
      'DynEarthSol finds static or quasi-static equilibrium through dynamic ' +
      'relaxation. Combined with explicit time marching, this keeps the ' +
      'overall algorithm simple.',
  },
  {
    title: 'Updated Lagrangian scheme',
    text:
      'Large deformations are simulated within small-strain kinematics, and ' +
      'free-boundary deformation is tracked naturally. Adaptive remeshing ' +
      'keeps the mesh usable as it distorts.',
  },
  {
    title: 'Various material models',
    text:
      'Linear elasticity, poro-elasticity, Mohr-Coulomb plasticity with strain ' +
      'or rate-and-state weakening, and Maxwell viscoelasticity. New material ' +
      'models are easy to add.',
  },
];

function HomepageHighlights() {
  return (
    <section className={styles.section}>
      <div className="container">
        <div className="row">
          {Highlights.map(({title, text}) => (
            <div key={title} className="col col--4">
              <Heading as="h3">{title}</Heading>
              <p>{text}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

type MoreLink = {title: string; text: string; to?: string; href?: string; label: string};

const MoreLinks: MoreLink[] = [
  {
    title: 'Generate an input file',
    text: 'A browser-based form that writes a ready-to-run .cfg configuration file. No installation required.',
    href: 'https://geoflac.github.io/des-inputgen/',
    label: 'Input generator',
  },
  {
    title: 'Visualize results',
    text: 'Convert output with 2vtk.py, or write the compressed VTKHDF format and open it directly in ParaView.',
    to: '/docs/usage/visualize',
    label: 'Visualization',
  },
  {
    title: 'Couple with surface processes',
    text: 'Two-way coupling with goSPL: DES supplies tectonic velocities, goSPL returns erosion and deposition.',
    to: '/docs/tutorial/couplinggospl',
    label: 'goSPL coupling',
  },
];

function HomepageMoreLinks() {
  return (
    <section className={styles.sectionTight}>
      <div className="container">
        <div className="row">
          {MoreLinks.map(({title, text, to, href, label}) => (
            <div key={title} className="col col--4 margin-bottom--md">
              <div className={clsx('card', styles.card)}>
                <div className="card__body">
                  <Heading as="h3">{title}</Heading>
                  <p>{text}</p>
                </div>
                <div className="card__footer">
                  <Link
                    className="button button--outline button--primary button--block"
                    {...(href ? {href} : {to})}>
                    {label}
                  </Link>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

const VIDEO_IDS = ['0AuTI7MZ05M', 'vfeiY5WuV9c', 'zr-4HIg7_14', '_VZUCwzfxPk'];
const PLAYLIST =
  'https://www.youtube.com/playlist?list=PLLxHSgtMeGthxjsfFTv4aPTzCfcOqNCYD';

function Video({id}: {id: string}) {
  const [playing, setPlaying] = useState(false);
  if (playing) {
    return (
      <div className={styles.video}>
        <iframe
          src={`https://www.youtube-nocookie.com/embed/${id}?autoplay=1&rel=0`}
          title="DynEarthSol simulation video"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
          allowFullScreen
        />
      </div>
    );
  }
  return (
    <a
      className={styles.video}
      href={`https://youtu.be/${id}`}
      onClick={(e) => {
        e.preventDefault();
        setPlaying(true);
      }}>
      <img src={`https://img.youtube.com/vi/${id}/hqdefault.jpg`} alt="Play simulation video" loading="lazy" />
      <span className={styles.play} aria-hidden="true">▶</span>
    </a>
  );
}

function HomepageVideos() {
  return (
    <section className={styles.section}>
      <div className="container">
        <Heading as="h2">Simulations</Heading>
        <div className={styles.videoGrid}>
          {VIDEO_IDS.map((id) => (
            <Video key={id} id={id} />
          ))}
        </div>
        <p className="text--center margin-top--md">
          <Link href={PLAYLIST}>More simulation videos on YouTube →</Link>
        </p>
      </div>
    </section>
  );
}

function HomepageQuickStart() {
  return (
    <section className={styles.section}>
      <div className={clsx('container', styles.narrow)}>
        <Heading as="h2" id="quick-start">
          Quick start
        </Heading>
        <p>
          Build the 2D executable and run a worked example.{' '}
          <Link to="/docs/usage">Installation</Link> has the complete build
          guide: every build option, the optional libraries, and the platform
          notes.
        </p>
        <p>
          <strong>1. Install the dependencies</strong> for your platform. The
          build finds everything on its own, with no paths to edit.
        </p>
        <CodeBlock language="bash">
          {`brew install libomp               # macOS (Homebrew)
sudo apt install g++ make         # Debian / Ubuntu
sudo dnf install gcc-c++ make     # Fedora / RHEL`}
        </CodeBlock>
        <p>
          <strong>2. Get the source</strong>, including the bundled submodules,
          and <strong>build</strong>. <code>make</code> on its own builds the 3D
          executable, <code>dynearthsol3d</code>; <code>ndims=2</code> builds the
          2D one used below.
        </p>
        <CodeBlock language="bash">
          {`git clone --recurse-submodules https://github.com/GeoFLAC/DynEarthSol.git
cd DynEarthSol
make ndims=2`}
        </CodeBlock>
        <p>
          <strong>3. Run an example.</strong>
        </p>
        <CodeBlock language="bash">
          {`mkdir quickstart
cd quickstart
cp ../examples/tectonics/core-complex.cfg .
OMP_NUM_THREADS=4 ../dynearthsol2d core-complex.cfg`}
        </CodeBlock>
        <p>
          The <Link to="/docs/getting-started/quickstart">Quickstart</Link> page
          explains this model and how to look at its output. More example
          configurations live in <code>examples/</code>, and{' '}
          <code>dynearthsol2d -h</code> lists every input parameter. To write
          your own input file from a form, use the{' '}
          <Link href="https://geoflac.github.io/des-inputgen/">input generator</Link>.
          If a build picks up an unexpected library, <code>make config</code>{' '}
          prints the compiler and every dependency path it resolved to, which
          is also the most useful thing to include in a bug report.
        </p>
      </div>
    </section>
  );
}

function HomepageCitation() {
  return (
    <section className={styles.section}>
      <div className={clsx('container', styles.narrow)}>
        <Heading as="h2" id="citing">
          Citing DynEarthSol
        </Heading>
        <p>Please cite the DynEarthSol v2.0 paper (preprint):</p>
        <blockquote>
          Shyu, C. J., Lee, S., Ding, X., Keum, J., Tan, E., Lavier, L. L., &amp;
          Choi, E. (2026). DynEarthSol v2.0: An efficient explicit Lagrangian
          solver for geodynamics, surface processes, and earthquake-cycle
          dynamics. <em>EGUsphere</em> [preprint].{' '}
          <Link href="https://doi.org/10.5194/egusphere-2026-2922">
            doi:10.5194/egusphere-2026-2922
          </Link>
        </blockquote>
        <p>and the original method paper:</p>
        <blockquote>
          Choi, E., Tan, E., Lavier, L. L., &amp; Calo, V. M. (2013).
          DynEarthSol2D: An efficient unstructured finite element method to
          study long-term tectonic deformation.{' '}
          <em>Journal of Geophysical Research: Solid Earth</em>, 118(5),
          2429–2444.{' '}
          <Link href="https://doi.org/10.1002/jgrb.50148">doi:10.1002/jgrb.50148</Link>
        </blockquote>
        <p>
          To cite the software itself, use{' '}
          <Link href="https://doi.org/10.5281/zenodo.20293557">
            doi:10.5281/zenodo.20293557
          </Link>
          . This DOI covers every archived release, both the software
          (<code>v2.x.x</code>) and the benchmark datasets
          (<code>benchmarks-v2.x.x</code>), and it opens the list of all
          versions. To cite the exact version you used, pick the matching
          software release from that list, or take its DOI from the{' '}
          <Link href="https://github.com/GeoFLAC/DynEarthSol/releases">releases page</Link>{' '}
          or from the <code>CITATION.cff</code> file shipped with that release.
        </p>
      </div>
    </section>
  );
}

export default function Home(): ReactNode {
  return (
    <Layout title="DynEarthSol" description={TAGLINE}>
      <HomepageHeader />
      <main>
        <HomepageHighlights />
        <HomepageFeatures />
        <HomepageMoreLinks />
        <HomepageVideos />
        <HomepageQuickStart />
        <HomepageCitation />
      </main>
    </Layout>
  );
}
