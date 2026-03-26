/**
 * Utility formatting functions for the RL Trading App
 * Centralized formatters for consistent output across all components
 */

export const fmt = (n, d = 2) => 
  Number(n).toLocaleString("en-US", { 
    minimumFractionDigits: d, 
    maximumFractionDigits: d 
  });

export const fmtUSD = (n) => `$${fmt(n)}`;

export const fmtPct = (n) => `${n >= 0 ? "+" : ""}${fmt(n)}%`;

export const rand = (min, max) => Math.random() * (max - min) + min;

export const randInt = (min, max) => Math.floor(rand(min, max));

export const randIntArray = (length, min, max) => 
  Array.from({ length }, () => randInt(min, max));
