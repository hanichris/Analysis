export default function About() {
  return (
    <section className="section">
      <div className="container">
        <article className="section-padding">
          <header className="section-header">
            <h1 className="section-title">What we do now</h1>
          </header>
          <p className="section-tagline">
            Divergent Space is a forward-thinking consultancy that leverages
            space technology to drive business growth and societal impact. By
            blending visionary strategies with innovative space solutions, we
            help businesses succeed while addressing global challenges. With a
            focus on creativity, collaboration, and excellence, we deliver real
            results, transforming bold ideas into profitable and purposeful
            realities. Join us in shaping a future where space technology fuels
            both business success and positive change.
          </p>
        </article>
        <article className="section-padding mt-b">
          <header className="section-header">
            <h1 className="section-title">Meet our Team</h1>
          </header>
          <div className="grid">
            <div>
              <div>
                <img
                  sizes="(max-width: 2633px) 40vw, 1053px"
                  srcSet="
                    static/analysis/img/ceo/ceo_c_scale,w_380.jpg 380w,
                    static/analysis/img/ceo/ceo_c_scale,w_659.jpg 659w,
                    static/analysis/img/ceo/ceo_c_scale,w_861.jpg 861w,
                    static/analysis/img/ceo/ceo_c_scale,w_1002.jpg 1002w,
                    static/analysis/img/ceo/ceo_c_scale,w_1053.jpg 1053w"
                  src="static/analysis/img/ceo/ceo_c_scale,w_1053.jpg"
                  alt="image of CEO Mr. Albert Mbogo"
                />
              </div>
              <div>
                <h3 className="grid-item-title">
                  CEO <br />
                  Mr. Albert Mbogo
                </h3>
                <div className="grid-item-tagline">
                  <span>
                    An entrepreneur, astrophysicist and our proud founder.
                  </span>
                </div>
              </div>
            </div>
            <div>
              <div>
                <img
                  sizes="(max-width: 6500px) 40vw, 2600px"
                  srcSet="
                    static/analysis/img/coo/coo_c_scale,w_380.jpg 380w,
                    static/analysis/img/coo/coo_c_scale,w_1185.jpg 1185w,
                    static/analysis/img/coo/coo_c_scale,w_1739.jpg 1739w,
                    static/analysis/img/coo/coo_c_scale,w_2278.jpg 2278w,
                    static/analysis/img/coo/coo_c_scale,w_2600.jpg 2600w"
                  src="static/analysis/img/coo/coo_c_scale,w_2600.jpg"
                  alt="image of COO Mr. Joshua Oleko"
                />
              </div>
              <div>
                <h3 className="grid-item-title">
                  COO <br />
                  Mr. Joshua Oleko
                </h3>
                <div className="grid-item-tagline">
                  <span>
                    A Biosystems engineer who has had international experience
                    in food production and sustainable agriculture.
                  </span>
                </div>
              </div>
            </div>
            <div>
              <div>
                <img
                  sizes="(max-width: 2133px) 40vw, 853px"
                  srcSet="
                  static/analysis/img/cto/cto_c_scale,w_380.jpg 380w,
                  static/analysis/img/cto/cto_c_scale,w_581.jpg 581w,
                  static/analysis/img/cto/cto_c_scale,w_853.jpg 853w"
                  src="cto/cto_c_scale,w_853.jpg"
                  alt="image of CTO Mr. Boniface Mwangi"
                />
              </div>
              <div>
                <h3 className="grid-item-title">
                  CTO <br />
                  Mr. Boniface Jacobi
                </h3>
                <div className="grid-item-tagline">
                  <span>
                    A data scientist with a wealth of experience in statistics
                    and software engineering.
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
