import { useEffect } from "react";
import 'bootstrap/dist/js/bootstrap.bundle.min.js';  

const useBootstrapTooltip = () => {
  useEffect(() => {
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    
    const tooltips = [...tooltipTriggerList].map(el => new bootstrap.Tooltip(el));

    return () => {
      tooltips.forEach(tooltip => tooltip.dispose());
    };
  }, []);
};

export default useBootstrapTooltip;
