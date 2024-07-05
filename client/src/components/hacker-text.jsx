import React, { useState, useEffect, useRef } from "react";

const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()+{}[]:;|\\?/<>~";

const HackerText = ({ text, styles }) => {
  const [displayText, setDisplayText] = useState(text);
  const intervalIdRef = useRef(null);

  const randomizeText = (event) => {
    const len = letters.length;
    let iteration = 0;
    const originalText = event.target.getAttribute("data-value");

    clearInterval(intervalIdRef.current);

    intervalIdRef.current = setInterval(() => {
      setDisplayText((prev) =>
        prev
          .split("")
          .map((letter, index) => {
            if (index < iteration) {
              return originalText[index];
            }
            return letters[Math.floor(Math.random() * len)];
          })
          .join("")
      );

      if (iteration >= originalText.length) {
        clearInterval(intervalIdRef.current);
      }

      iteration += 1 / 3;
    }, 30);
  };

  const resetText = () => {
    clearInterval(intervalIdRef.current);
    setDisplayText(text);
  };

  useEffect(() => {
    return () => clearInterval(intervalIdRef.current); // Cleanup on unmount
  }, []);

  return (
    <h1
      data-value={text}
      onMouseEnter={randomizeText}
      onMouseLeave={resetText}
      className={`cursor-pointer font-mono text-gray-950 transition-all duration-150 ease-in ${styles}`}
    >
      {displayText}
    </h1>
  );
};

export default HackerText;
