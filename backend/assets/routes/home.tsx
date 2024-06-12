export default function HomePage() {
  return (
    <>
      <section>
        <div>
          <video autoPlay loop>
            <source src='/static/analysis/img/landing_anim.mp4' type="video/mp4" />
          </video>
        </div>
        <span>
          <span>
            Welcome to <br />
            <span>
              Divergent Space
            </span>
          </span>
          <span>
            Elevating Business through Space Excellence and Societal Innovation
          </span>
        </span>
      </section>


      <span>
        We are a leading consultancy that harnesses space technology to propel
        businesses forward and initiates visionary projects to create positive
        societal impact.
      </span>


      <div>
        <div>
          <div>
            <img
              src="/static/analysis/img/satellite_arial.jpg"
              alt="statellit arial image."
            />
          </div>
          <div>
            <h2>
              Data from above
            </h2>
            <p>
              Satellite data unleashes a world of excitement, empowering us with
              real-time insights crucial for everything from predicting storms
              and managing disasters to revolutionizing agriculture and urban
              planning.
            </p>
          </div>
        </div>

        <div>
          <div>
            <h2>
              Fuelling progress
            </h2>
            <p>
              These orbiting eyes in the sky provide a dynamic perspective,
              fueling scientific breakthroughs and transforming how we
              understand and interact with our planet.
            </p>
          </div>
          <div>
            <img
              src="/static/analysis/img/satellite_side.jpg"
              alt="statellite side image"
            />
          </div>
        </div>
      </div>


      <div>
        <h2>
          A sneak peak into how we work
        </h2>
        <div>
          <img src="/static/analysis/img/software.jpg" />
        </div>
      </div>
    </>
  );
}