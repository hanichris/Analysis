export default function About() {
  return (
    <section className="section">
      <div className="container">
        <article className="section-padding">
          <header className="section-header">
            <h1 className="section-title">
              What we do now
            </h1>
          </header>
          <p className="section-tagline">
            Divergent Space is a pioneering consultancy dedicated to harnessing
            space technology's transformative potential for business growth and
            positive societal change. Our mission revolves around seamlessly
            integrating cutting-edge space solutions with visionary initiatives,
            creating a unique synergy between profit-driven success and societal
            impact. Specializing in strategic space consultancy, precise
            implementation plans, and innovative projects, we are architects of a
            transformative future. Our approach emphasizes divergent thinking,
            unlocking creativity for space-driven business success, with a proven
            track record of delivering tangible results in both profit and
            societal transformation. Focused on impact, collaboration, and
            excellence, Divergent Space invites individuals to engage by joining
            STEM committees or supporting initiatives contributing to real-world
            positive change. Our impact areas span space-powered business growth,
            innovative projects addressing societal challenges, and excellence in
            turning dreams into reality through space technology. Join us at
            Divergent Space, where the convergence of space and societal
            transformation shapes a future that is profitable and purposeful.
          </p>
        </article>
        <article className="section-padding mt-b">
          <header className="section-header">
            <h1 className="section-title">
              Meet our Team
            </h1>
          </header>
          <div className="grid">
            <div>
              <div>
                <img
                  sizes="(max-width: 2633px) 40vw, 1053px"
                  srcSet="
                    ceo/ceo_c_scale,w_380.jpg 380w,
                    ceo/ceo_c_scale,w_659.jpg 659w,
                    ceo/ceo_c_scale,w_861.jpg 861w,
                    ceo/ceo_c_scale,w_1002.jpg 1002w,
                    ceo/ceo_c_scale,w_1053.jpg 1053w"
                  src="ceo/ceo_c_scale,w_1053.jpg"
                  alt="image of CEO Mr. Albert Mbogo" />
              </div>
              <div>
                <h3 className="grid-item-title">
                  CEO <br />
                  Mr. Albert Mbogo
                </h3>
                <div className="grid-item-tagline">
                  <span>An entrepreneur, astrophysicist and our proud founder.</span>
                </div>
              </div>
            </div>
            <div>
              <div>
                <img
                  sizes="(max-width: 6500px) 40vw, 2600px"
                  srcSet="
                    coo/coo_c_scale,w_380.jpg 380w,
                    coo/coo_c_scale,w_1185.jpg 1185w,
                    coo/coo_c_scale,w_1739.jpg 1739w,
                    coo/coo_c_scale,w_2278.jpg 2278w,
                    coo/coo_c_scale,w_2600.jpg 2600w"
                  src="coo/coo_c_scale,w_2600.jpg"
                  alt="image of COO Mr. Joshua Oleko" />
              </div>
              <div>
                <h3 className="grid-item-title">
                  COO <br />
                  Mr. Joshua Oleko
                </h3>
                <div className="grid-item-tagline">
                  <span>
                    A Biosystems engineer who has had international experience in food
                    production and sustainable agriculture.
                  </span>
                </div>
              </div>
            </div>
            <div>
              <div>
                <img
                  sizes="(max-width: 2133px) 40vw, 853px"
                  srcSet="
                  cto/cto_c_scale,w_380.jpg 380w,
                  cto/cto_c_scale,w_581.jpg 581w,
                  cto/cto_c_scale,w_853.jpg 853w"
                  src="cto/cto_c_scale,w_853.jpg"
                  alt="image of CTO Mr. Boniface Mwangi"/>
              </div>
              <div>
                <h3 className="grid-item-title">
                  CTO <br />
                  Mr. Boniface Jacobi
                </h3>
                <div className="grid-item-tagline">
                  <span>
                    A data scientist with a wealth of experience in statistics and
                    software engineering.
                  </span>
                </div>
              </div>
            </div>
          </div>
        </article>
      </div>
    </section>
  );
}