/**
 * Centralized API Server URL Configuration for SORTIFY.
 * Automatically adapts to dynamic server host & port when embedded in PyWebView or browser.
 */
export const SERVER_BASE = (typeof window !== 'undefined' && window.location.origin && window.location.origin.startsWith('http'))
  ? window.location.origin
  : 'http://127.0.0.1:5000';

export const API_BASE = `${SERVER_BASE}/api`;
