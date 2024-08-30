/** @type {import('next').NextConfig} */
const nextConfig = {
    experimental: {
        serverActions: {
          allowedOrigins: ['localhost:8001', '*.localhost:8001', '127.0.0.1:8001', '*.127.0.0.1:8001'],
        },
      },
      productionBrowserSourceMaps: true,
};

export default nextConfig;
