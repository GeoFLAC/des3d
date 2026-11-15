import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

type FeatureItem = {
  title: string;
  Svg: React.ComponentType<React.ComponentProps<'svg'>>;
  description: ReactNode;
  link: string;
};

const FeatureList: FeatureItem[] = [
  {
    title: 'What is DynEarthSol?',
    Svg: require('@site/static/img/card-intro-mesh.svg').default,
    description: (
      <>
        Explicit Lagrangian finite element code for tectonics, earthquake
        cycles and surface processes.
      </>
    ),
    link: '/docs/intro',
  },
  {
    title: 'Getting started',
    Svg: require('@site/static/img/card-quickstart-terminal.svg').default,
    description: (
      <>
        Install DynEarthSol, run a first model and look at the results.
      </>
    ),
    link: '/docs/category/getting-started',
  },
  {
    title: 'Tutorials',
    Svg: require('@site/static/img/card-tutorials-book.svg').default,
    description: (
      <>
        Reproducible worked examples, from basic mechanics to tectonic and
        earthquake-cycle models.
      </>
    ),
    link: '/docs/category/tutorial',
  },
  {
    title: 'Theory',
    Svg: require('@site/static/img/card-theory-atom.svg').default,
    description: (
      <>
        Theoretical and numerical foundations: time integration, remeshing,
        constitutive laws, and more.
      </>
    ),
    link: '/docs/category/theory',
  },
];

function Feature({title, Svg, description, link}: FeatureItem) {
  return (
    <div className={clsx('col col--3')}>
      <Link to={link} className={styles.featureLink}>
        <div className="text--center">
          <Svg className={styles.featureSvg} role="img" />
        </div>
        <div className="text--center padding-horiz--md">
          <Heading as="h3">{title}</Heading>
          <p>{description}</p>
        </div>
      </Link>
    </div>
  );
}

export default function HomepageFeatures(): ReactNode {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
