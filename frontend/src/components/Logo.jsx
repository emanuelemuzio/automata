import { useEffect, useState } from "react";

const Logo = ({ width = 50, height = 50, className = "" }) => {
  const [svgContent, setSvgContent] = useState("");

  useEffect(() => {
    fetch("/logo.svg")   
      .then((response) => response.text())
      .then((data) => {
        const parser = new DOMParser();
        const doc = parser.parseFromString(data, "image/svg+xml");
        const svgElement = doc.querySelector("svg");

        if (svgElement) {
          svgElement.setAttribute("width", width);   
          svgElement.setAttribute("height", height); 
          
          const existingClass = svgElement.getAttribute("class") || "";
          svgElement.setAttribute("class", `${existingClass} ${className}`.trim());

          setSvgContent(svgElement.outerHTML);
        }
      })
      .catch((error) => console.error("Errore nel caricamento del logo:", error));
  }, [width, height, className]);  

  return <div dangerouslySetInnerHTML={{ __html: svgContent }} />;
};

export default Logo;
