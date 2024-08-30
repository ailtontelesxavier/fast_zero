import { NextRequest, NextResponse } from "next/server"

export default function middleware(request: NextRequest) {

    //console.log(request.cookies.get('next-auth.session-token'));

    //const token = request.cookies.get('auth_token')?.value;
    const token = request.cookies.get('next-auth.session-token')?.value;

    const signInURL = new URL('/authentication', request.url);
    const dashboardURL = new URL('/app', request.url);

    if (!token) {
        if (request.nextUrl.pathname === '/') {
            return NextResponse.next();
        }
        if (request.nextUrl.pathname === '/authentication') {
            return NextResponse.next();
        }
        return NextResponse.redirect(signInURL);
    }

    if (request.nextUrl.pathname === '/') {
        return NextResponse.redirect(dashboardURL)
    }
}

export const config = {
    // https://nextjs.org/docs/app/building-your-application/routing/middleware#matcher

    //matcher: ['/', '/dashboard/:path*']
    //matcher: ["/app"]
    matcher: ['/((?!api|_next/static|_next/image|.*\\.png$).*)'],
}

/*
  'use client'
  const pathname = usePathname();
  const isPublicPage = checkIsPublicRoute(pathname!);

  console.log(isPublicPage)
  */
