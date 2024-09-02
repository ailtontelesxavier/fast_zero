/** @type {import('next').NextConfig} */
const nextConfig = {
    experimental: {
        serverActions: {
          allowedOrigins: ['localhost:8002', '*.localhost:8002', '127.0.0.1:8002', '*.127.0.0.1:8002'],
        },
      },
      productionBrowserSourceMaps: true,
      swcMinify: false,
};

export default nextConfig;
