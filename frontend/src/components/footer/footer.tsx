export default function Footer() {
  // Divergent Space &copy; 2024
  return (
    <footer className="footer" data-section-theme="gold">
      <div className="container">
        <div className="footer-row">
          <div className="col-1-2">
            <svg
              width="90"
              height="90"
              viewBox="0 0 512 512"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <g clipPath="url(#clip0_1_18)">
                <path
                  fillRule="evenodd"
                  clipRule="evenodd"
                  d="M263.505 259.501C265.112 262.105 267.253 260.623 269.04 255.668L270.678 251.129L270.778 256.078C270.833 258.8 271.248 261.027 271.7 261.027C275.767 261.027 306.952 268.337 314.552 271.071C334.747 278.339 354.131 289.963 371.822 305.421C377.285 310.192 382.138 313.457 383.118 313.016C385.308 312.033 408.256 286.78 417.081 275.643C433.267 255.216 440.162 239.531 435.453 233.845C430.615 228.007 409.849 237.699 366.463 266.044C358.532 271.227 351.715 275.121 351.313 274.7C350.911 274.279 351.906 273.044 353.523 271.955C355.14 270.867 361.201 266.328 366.994 261.871C392.193 242.482 407.351 232.889 419.748 228.489C433.813 223.497 440.848 224.717 443.443 232.598C446.075 240.585 442.717 253.633 435.151 264.826C423.929 281.426 390.371 316.545 362.44 340.918C352.55 349.548 315.273 380.04 310.471 383.427C310.147 383.656 314.89 388.927 321.01 395.142L332.139 406.44L367.709 405.897C407.159 405.295 410.833 404.62 411.61 397.844C412.669 388.612 400.799 358.061 387.277 335.217C381.864 326.071 386.288 321.668 392.536 329.983C403.103 344.045 414.494 371.119 418.984 392.851C420.196 398.717 420.456 402.374 422.349 404.695C425.929 409.084 435.345 408.694 468.07 409.427C491.852 409.96 511.557 410.638 511.859 410.935C512.16 411.234 511.963 411.921 511.42 412.466C510.137 413.752 72.269 414.638 40.4333 413.42C27.0864 412.91 17.0081 412.04 18.037 411.488C19.0659 410.935 37.6878 410.059 59.4201 409.54C81.1511 409.023 99.3277 408.353 99.8126 408.053C100.297 407.753 101.374 403.204 102.205 397.944C105.765 375.432 116.881 346.214 126.388 334.389C129.536 330.472 132.548 330.571 132.548 334.59C132.548 335.768 129.058 344.196 124.791 353.318C115.373 373.46 111.469 385.693 111.469 395.072C111.469 401.053 111.926 402.393 114.433 403.747C116.469 404.846 128.54 405.518 152.968 405.891L188.539 406.434L197.281 399.083C202.089 395.039 206.358 390.857 206.767 389.788C207.275 388.462 201.161 382.508 187.486 371.016C118.924 313.395 65.3591 264.67 65.3591 259.926C65.3591 256.933 68.3088 256.995 72.3323 260.072C77.6231 264.117 81.9732 268.139 100.93 286.505C109.262 294.578 120.321 305.29 125.504 310.309L134.929 319.435L147.9 307.831C171.889 286.371 196.179 272.899 222.749 266.316C231.413 264.17 239.414 261.977 240.527 261.444C241.642 260.91 244.332 260.45 246.506 260.421C249.822 260.376 250.525 259.782 250.874 256.737C251.408 252.095 253.449 252.029 253.994 256.636C254.591 261.686 257.205 261.875 258.191 256.938C258.651 254.632 259.471 243.177 260.012 231.482L260.998 210.217L261.738 234.026C262.145 247.121 262.939 258.584 263.505 259.501ZM185.099 289.591C194.507 284.068 213.216 276.552 226.273 273.049C231.604 271.619 237.448 270.556 239.26 270.687C242.32 270.907 242.523 271.346 242.125 276.863C241.029 292.092 232.793 333.74 228.423 346.149C222.842 362 211.321 383.766 208.516 383.757C204.847 383.743 144.405 328.375 144.405 325.028C144.405 320.993 170.872 297.944 185.099 289.591ZM243.218 291.461C244.664 280.98 245.847 271.924 245.847 271.335C245.847 270.746 246.428 270.265 247.14 270.265C249.747 270.265 249.928 276.877 247.868 296.769C241.867 354.752 225.81 400.33 209.856 404.669C207.552 405.297 205.254 405.586 204.752 405.312C204.249 405.039 207.302 399.632 211.533 393.298C227.906 368.792 236.247 341.986 243.218 291.461ZM251.013 293.125C251.687 283.56 253.01 274.355 253.951 272.669C255.575 269.761 255.708 269.941 256.567 276.204C257.065 279.833 257.525 309.264 257.588 341.608C257.678 387.189 257.329 400.929 256.032 402.704C254.69 404.542 251.679 405.115 240.77 405.605C233.295 405.94 226.665 405.897 226.037 405.507C225.41 405.119 227.159 400.215 229.926 394.611C236.516 381.262 239.795 370.852 243.737 350.769C247.504 331.572 249.309 317.274 251.013 293.125ZM264.122 373.53C262.929 337.507 262.746 277.189 263.818 273.18C264.262 271.517 265.275 270.373 266.067 270.638C268.122 271.324 269.102 277.188 271.408 302.598C273.77 328.634 277.459 351.505 282.155 369.245C285.62 382.327 292.387 398.538 295.446 401.081C296.426 401.895 297.227 403.323 297.227 404.252C297.227 406.559 269.013 406.176 266.678 403.838C265.58 402.737 264.775 393.184 264.122 373.53ZM273.5 292.446C272.783 287.588 272.196 280.61 272.196 276.939C272.196 270.819 273.572 268.478 275.417 271.466C275.824 272.127 277.352 281.777 278.812 292.911C285.357 342.84 295.485 374.095 312.3 396.251C318.906 404.956 318.606 407.373 311.225 404.932C305.299 402.973 301.007 397.863 294.655 385.203C286.931 369.811 281.52 348.707 276.861 315.796C275.73 307.811 274.218 297.303 273.5 292.446ZM293.259 344.12C287.034 323.912 281.551 297.546 280.575 283.132C279.825 272.045 279.986 270.265 281.734 270.265C284.908 270.265 307.837 276.457 313.695 278.897C337.316 288.733 348.19 295.803 370.344 315.722L375.614 320.46L371.662 323.892C369.488 325.781 363.856 330.966 359.145 335.417C354.434 339.869 344.948 348.557 338.066 354.724C331.184 360.892 323.049 368.248 319.991 371.07C309.89 380.39 309.852 380.401 306.019 374.819C301.576 368.346 298.281 360.421 293.259 344.12Z"
                  fill="currentColor"
                />
                <path
                  d="M21.0803 167.275C30.9531 170.679 36.3796 173.667 56.307 186.681C81.9073 203.398 110.658 225.16 145.712 254.355C176.708 280.172 173.128 278.685 134.249 249.598C94.7075 220.014 92.0002 218.067 69.9701 203.34C33.0952 178.688 10.3076 168.132 6.67546 174.016C5.38833 176.103 12.9003 190.277 21.5519 202.083L29.1298 212.426L39.2885 211.566C51.4523 210.535 56.477 212.39 63.3711 220.459C77.1 236.526 65.7714 260.938 44.5569 261.005C26.4435 261.061 18.0607 248.698 21.0618 226.352L22.2633 217.412L13.6803 204.576C2.62438 188.044 -0.835194 181.085 -0.993285 175.06C-1.25941 164.91 6.3896 162.213 21.0803 167.275Z"
                  fill="currentColor"
                />
                <path
                  d="M377.088 178.705C384.803 182.373 389.555 191.808 387.607 199.586C386.19 205.239 379.441 211.704 373.1 213.482C367.804 214.968 366.782 214.853 362.191 212.269C354.256 207.8 350.773 201.719 351.543 193.68C352.8 180.582 365.442 173.17 377.088 178.705Z"
                  fill="currentColor"
                />
                <path
                  d="M412.58 162.173C413.071 162.969 412.513 164.58 411.34 165.755C409.376 167.723 409.027 167.709 406.903 165.581C404.886 163.56 404.845 163.114 406.574 162.019C409.211 160.348 411.49 160.407 412.58 162.173Z"
                  fill="currentColor"
                />
                <path
                  d="M270.673 195.619C270.922 196.906 270.476 198.61 269.685 199.403C267.532 201.559 265.147 198.573 266.249 195.101C267.283 191.834 270.002 192.154 270.673 195.619Z"
                  fill="currentColor"
                />
                <path
                  d="M255.069 196.282C255.069 199.341 252.704 201.117 250.959 199.369C249.305 197.712 250.913 193.72 253.234 193.72C254.243 193.72 255.069 194.872 255.069 196.282Z"
                  fill="currentColor"
                />
                <path
                  d="M247.682 216.924C249.044 220.48 248.57 222.754 246.465 222.754C244.083 222.754 242.615 219.616 243.689 216.815C244.677 214.233 246.672 214.287 247.682 216.924Z"
                  fill="currentColor"
                />
                <path
                  d="M277.983 216.924C279.446 220.74 278.812 222.754 276.148 222.754C273.3 222.754 273.138 222.312 274.343 217.805C275.271 214.34 276.848 213.958 277.983 216.924Z"
                  fill="currentColor"
                />
                <path
                  d="M262.756 134.848C262.999 136.1 262.808 138.13 262.332 139.358C261.531 141.427 261.34 141.416 259.725 139.22C257.759 136.545 258.571 131.323 260.836 132.078C261.65 132.35 262.514 133.596 262.756 134.848Z"
                  fill="currentColor"
                />
                <path
                  d="M183.979 164.654C181.302 166.312 179.53 164.834 181.437 162.533C182.579 161.156 183.429 161.018 184.453 162.045C185.48 163.073 185.347 163.808 183.979 164.654Z"
                  fill="currentColor"
                />
                <path
                  d="M179.976 200.241C179.976 203.42 177.587 205.053 175.701 203.163C174.699 202.16 174.778 201.161 175.977 199.714C178.28 196.936 179.976 197.159 179.976 200.241Z"
                  fill="currentColor"
                />
                <path
                  d="M75.0435 144.473L79.8969 149.336L75.6627 153.711C73.3348 156.118 70.837 158.087 70.1137 158.087C68.015 158.087 61.4068 151.193 61.4068 149.005C61.4068 147.042 67.6817 139.611 69.3377 139.611C69.8067 139.611 72.3744 141.799 75.0435 144.473Z"
                  fill="currentColor"
                />
                <path
                  d="M28.471 337.571C28.471 338.297 27.8782 338.891 27.1536 338.891C26.429 338.891 25.8362 338.297 25.8362 337.571C25.8362 336.845 26.429 336.251 27.1536 336.251C27.8782 336.251 28.471 336.845 28.471 337.571Z"
                  fill="currentColor"
                />
                <path
                  d="M437.362 101.632C439.37 104.825 436.715 107.196 432.36 106.1C428.705 105.18 427.998 102.84 430.589 100.245C432.673 98.1568 435.548 98.7467 437.362 101.632Z"
                  fill="currentColor"
                />
                <path
                  d="M464.433 288.539C465.969 291.413 463.995 294.02 460.284 294.02C457.559 294.02 455.975 291.051 457.113 288.081C458.172 285.315 462.866 285.608 464.433 288.539Z"
                  fill="currentColor"
                />
                <path
                  d="M506.435 327.277C508.663 329.509 508.399 333.182 505.945 334.125C503.39 335.107 498.794 332.796 498.794 330.53C498.794 328.476 501.446 325.694 503.405 325.694C504.202 325.694 505.565 326.406 506.435 327.277Z"
                  fill="currentColor"
                />
              </g>
              <defs>
                <clipPath id="clip0_1_18">
                  <rect width="512" height="512" fill="white" />
                </clipPath>
              </defs>
            </svg>
            <address className="footer-address"></address>
          </div>
          <div className="col-1-2">
            <ul className="social nav">
              <li className="social-item nav-item">
                <a href="" className="social-link">
                  <svg
                    viewBox="0 0 24 24"
                    xmlns="http://www.w3.org/2000/svg"
                    width="25"
                    height="25"
                  >
                    <title>Facebook icon</title>
                    <path d="M23.998 12c0-6.628-5.372-12-11.999-12C5.372 0 0 5.372 0 12c0 5.988 4.388 10.952 10.124 11.852v-8.384H7.078v-3.469h3.046V9.356c0-3.008 1.792-4.669 4.532-4.669 1.313 0 2.686.234 2.686.234v2.953H15.83c-1.49 0-1.955.925-1.955 1.874V12h3.328l-.532 3.469h-2.796v8.384c5.736-.9 10.124-5.864 10.124-11.853z" />
                  </svg>
                </a>
              </li>
              <li className="social-item nav-item">
                <a href="https://x.com/divergent_space" className="social-link">
                  <svg
                    viewBox="0 0 24 24"
                    xmlns="http://www.w3.org/2000/svg"
                    width="25"
                    height="25"
                  >
                    <title>Twitter icon</title>
                    <path d="M23.954 4.569a10 10 0 0 1-2.825.775 4.958 4.958 0 0 0 2.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 0 0-8.384 4.482C7.691 8.094 4.066 6.13 1.64 3.161a4.822 4.822 0 0 0-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 0 1-2.228-.616v.061a4.923 4.923 0 0 0 3.946 4.827 4.996 4.996 0 0 1-2.212.085 4.937 4.937 0 0 0 4.604 3.417 9.868 9.868 0 0 1-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 0 0 7.557 2.209c9.054 0 13.999-7.496 13.999-13.986 0-.209 0-.42-.015-.63a9.936 9.936 0 0 0 2.46-2.548l-.047-.02z" />
                  </svg>
                </a>
              </li>
              <li className="social-item nav-item">
                <a
                  href="https://www.instagram.com/divergent.space?igsh=MW83ZThyNTAxeGhnbg=="
                  className="social-link"
                >
                  <svg
                    viewBox="0 0 24 24"
                    xmlns="http://www.w3.org/2000/svg"
                    width="25"
                    height="25"
                  >
                    <title>Instagram icon</title>
                    <path d="M12 0C8.74 0 8.333.015 7.053.072 5.775.132 4.905.333 4.14.63c-.789.306-1.459.717-2.126 1.384S.935 3.35.63 4.14C.333 4.905.131 5.775.072 7.053.012 8.333 0 8.74 0 12s.015 3.667.072 4.947c.06 1.277.261 2.148.558 2.913a5.885 5.885 0 0 0 1.384 2.126A5.868 5.868 0 0 0 4.14 23.37c.766.296 1.636.499 2.913.558C8.333 23.988 8.74 24 12 24s3.667-.015 4.947-.072c1.277-.06 2.148-.262 2.913-.558a5.898 5.898 0 0 0 2.126-1.384 5.86 5.86 0 0 0 1.384-2.126c.296-.765.499-1.636.558-2.913.06-1.28.072-1.687.072-4.947s-.015-3.667-.072-4.947c-.06-1.277-.262-2.149-.558-2.913a5.89 5.89 0 0 0-1.384-2.126A5.847 5.847 0 0 0 19.86.63c-.765-.297-1.636-.499-2.913-.558C15.667.012 15.26 0 12 0zm0 2.16c3.203 0 3.585.016 4.85.071 1.17.055 1.805.249 2.227.415.562.217.96.477 1.382.896.419.42.679.819.896 1.381.164.422.36 1.057.413 2.227.057 1.266.07 1.646.07 4.85s-.015 3.585-.074 4.85c-.061 1.17-.256 1.805-.421 2.227a3.81 3.81 0 0 1-.899 1.382 3.744 3.744 0 0 1-1.38.896c-.42.164-1.065.36-2.235.413-1.274.057-1.649.07-4.859.07-3.211 0-3.586-.015-4.859-.074-1.171-.061-1.816-.256-2.236-.421a3.716 3.716 0 0 1-1.379-.899 3.644 3.644 0 0 1-.9-1.38c-.165-.42-.359-1.065-.42-2.235-.045-1.26-.061-1.649-.061-4.844 0-3.196.016-3.586.061-4.861.061-1.17.255-1.814.42-2.234.21-.57.479-.96.9-1.381.419-.419.81-.689 1.379-.898.42-.166 1.051-.361 2.221-.421 1.275-.045 1.65-.06 4.859-.06l.045.03zm0 3.678a6.162 6.162 0 1 0 0 12.324 6.162 6.162 0 1 0 0-12.324zM12 16c-2.21 0-4-1.79-4-4s1.79-4 4-4 4 1.79 4 4-1.79 4-4 4zm7.846-10.405a1.441 1.441 0 0 1-2.88 0 1.44 1.44 0 0 1 2.88 0z" />
                  </svg>
                </a>
              </li>
              <li className="social-item nav-item">
                <a
                  href="https://www.linkedin.com/company/divergentspaceltd"
                  className="social-link"
                >
                  <svg
                    fill="currentColor"
                    height="25"
                    width="25"
                    version="1.1"
                    id="Layer_1"
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 310 310"
                  >
                    <title>LinkedIn icon</title>
                    <g id="XMLID_801_">
                      <path
                        id="XMLID_802_"
                        d="M72.16,99.73H9.927c-2.762,0-5,2.239-5,5v199.928c0,2.762,2.238,5,5,5H72.16c2.762,0,5-2.238,5-5V104.73
		C77.16,101.969,74.922,99.73,72.16,99.73z"
                      />
                      <path
                        id="XMLID_803_"
                        d="M41.066,0.341C18.422,0.341,0,18.743,0,41.362C0,63.991,18.422,82.4,41.066,82.4
		c22.626,0,41.033-18.41,41.033-41.038C82.1,18.743,63.692,0.341,41.066,0.341z"
                      />
                      <path
                        id="XMLID_804_"
                        d="M230.454,94.761c-24.995,0-43.472,10.745-54.679,22.954V104.73c0-2.761-2.238-5-5-5h-59.599
		c-2.762,0-5,2.239-5,5v199.928c0,2.762,2.238,5,5,5h62.097c2.762,0,5-2.238,5-5v-98.918c0-33.333,9.054-46.319,32.29-46.319
		c25.306,0,27.317,20.818,27.317,48.034v97.204c0,2.762,2.238,5,5,5H305c2.762,0,5-2.238,5-5V194.995
		C310,145.43,300.549,94.761,230.454,94.761z"
                      />
                    </g>
                  </svg>
                </a>
              </li>
            </ul>
          </div>
        </div>
        <hr />
        <div className="footer-row">
          <div className="col-1-2">
            <p className="footer-copyright">
              Divergent Space &copy; {new Date().getFullYear()}
            </p>
          </div>
          <div className="col-1-2">
            <ul className="footer-nav nav">
              <li className="footer-nav-item nav-item">
                <a href="" className="footer-nav-link">
                  Terms of use.
                </a>
              </li>
              <li className="footer-nav-item nav-item">
                <a href="" className="footer-nav-link">
                  Privacy Policy.
                </a>
              </li>
              <li className="footer-nav-item nav-item">
                <a href="" className="footer-nav-link">
                  Cookie Policy.
                </a>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </footer>
  );
}
