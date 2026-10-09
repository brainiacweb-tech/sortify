/**
 * Centralized API Server URL Configuration for SORTIFY.
 * Automatically adapts to dynamic server host & port when embedded in PyWebView or browser.
 */
export const SERVER_BASE = import.meta.env.DEV
  ? 'http://127.0.0.1:5000'
  : window.location.origin;

export const API_BASE = `${SERVER_BASE}/api`;
