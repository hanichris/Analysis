export default function AboutPage() {
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
          <div>
            <img
              src="/static/analysis/img/satellite_side.jpg"
              alt="statellite-image"
            />
          </div>
        </article>

        <article className="section-padding mt-b">
          <header className="section-header">
            <h1 className="section-title">
              Who we are
            </h1>
          </header>
          <div className="grid">
            <div>
              <div>
                <img src="/static/analysis/img/ceo.jpg" alt="image of CEO Mr. Albert Mbogo"/>
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
                <img src="/static/analysis/img/coo.jpg" alt="image of COO Mr. Joshua Oleko"/>
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
                <img src="/static/analysis/img/cto.jpeg" alt="image of CTO Ms. Evelyn"/>
              </div>
              <div>
                <h3 className="grid-item-title">
                  CTO <br />
                  Ms. Evelyn
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


        <article className="section-padding mt-b">
          <header className="section-header">
            <h1 className="section-title">
              Our Approach
            </h1>
          </header>
          <div>
            <ol>
              <li>
                Divergent Space Consultancy: Craft business strategies powered by
                space technology.
              </li>
              <li>
                Implementation Expertise: Seamlessly execute strategies for
                tangible, real-world impact.
              </li>
              <li>
                Innovative Initiatives: Turning dreams into reality through space
                technology.
              </li>
            </ol>
          </div>
        </article>

        <article className="section-padding mt-b">
          <header className="section-header">
            <h1 className="section-title">
              Why Choose Us
            </h1>
          </header>
          <div data-item="space-around" className="grid">
            <div>
              <div className="img-background">
                <img src="/static/analysis/img/divergent.svg" alt="divergent image"/>
              </div>
              <div>
                <h3 className="grid-item-title">Divergent Thinking</h3>
                <div className="grid-item-tagline">
                  <span>Unleashing creativity for space-driven business success</span>
                </div>
              </div>
            </div>
            <div>
              <div className="img-background">
                <img src="/static/analysis/img/profit.svg" alt="profit image"/>
              </div>
              <div>
                <h3 className="grid-item-title">Proven Impact</h3>
                <div className="grid-item-tagline">
                  <span>
                    Tangible results in both profit and societal transformation
                  </span>
                </div>
              </div>
            </div>
          </div>

          <div>
            <div>
              <h1>
                Get Involved
              </h1>
              <h2>
                Join a Committee
              </h2>
              <span>
                Contribute to impactful projects through our STEM committees
              </span>
              <h2>
                Support Our Projects
              </h2>
              <span>
                Be part of the change and support initiatives that transform lives.
              </span>
            </div>

            <div>
              <header>
                <h1>
                  Impact Areas
                </h1>
              </header>

              <div>
                <span>
                  Space-Powered Business
                </span>
                : Competitive advantage and success for our clients.

                <span>
                  Societal Development
                </span>
                : Innovative projects addressing real-world challenges.

                <span>
                  Innovation Excellence
                </span>
                : Turning dreams into reality through space technology.
              </div>
            </div>
          </div>
      
          <div>
            <p>
              Join us at Divergent Space Strategies, where space and societal
              transformation converge for a future that's both profitable and
              purposeful.
            </p>
          </div>
        </article>
      </div>
    </section>
  );
}