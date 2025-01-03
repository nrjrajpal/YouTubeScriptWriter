import { clerkMiddleware, createRouteMatcher } from '@clerk/nextjs/server'
import { NextRequest, NextResponse } from 'next/server'

const isOnboardingRoute = createRouteMatcher(['/onboarding'])
const isPublicRoute = createRouteMatcher(['/sign-in', '/sign-up', '/'])
const isHomeRoute = createRouteMatcher(['/'])

async function handleProjectMiddleware(request: Request, userEmail: string) {
  console.log("The project middleware")
  const url = new URL(request.url);
  console.log('URL:', url.pathname);
  if (url.pathname === '/onboarding') {
    return NextResponse.next();
  }
  const projectId = url.pathname.split('/')[3];

  if (url.pathname.startsWith('/project/') && projectId) {
    try {
      // Prepare the payload for the POST request (including userEmail in the body)
      const requestBody = JSON.stringify({ userEmail });

      // Check if the project exists
      const checkProjectUrl = `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/checkProject/${projectId}`;
      const checkProjectResponse = await fetch(checkProjectUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: requestBody,
      });

      if (checkProjectResponse.status === 404) {
        console.error(`Project ${projectId} does not exist. Redirecting to dashboard.`);
        url.pathname = '/dashboard';
        return NextResponse.redirect(url);
      }
      if (!checkProjectResponse.ok) {
        console.error("API Error (Check Project):", await checkProjectResponse.text());
        return NextResponse.next();
      }

      // Get the next stage for the project
      const getNextStageUrl = `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/getNextStage/${projectId}`;
      const getNextStageResponse = await fetch(getNextStageUrl);
      if (!getNextStageResponse.ok) {
        console.error("API Error (Get Next Stage):", await getNextStageResponse.text());
        return NextResponse.next();
      }

      const { next_stage } = await getNextStageResponse.json();
      const expectedPath = `/project/${next_stage}/${projectId}`;

      // Redirect to the correct stage if the current path is incorrect
      if (url.pathname !== expectedPath) {
        url.pathname = expectedPath;
        return NextResponse.redirect(url);
      }
    } catch (error) {
      console.error("Middleware Error:", error);
    }
  }
  return NextResponse.next();
}

export default clerkMiddleware(async (auth, req: NextRequest) => {
  // console.log("The clerk middleware")
  // First check project middleware if it's a project route
  const { userId, sessionClaims, redirectToSignIn } = await auth();
  if (req.nextUrl.pathname === '/onboarding') {
    return NextResponse.next();
  }
  if (req.nextUrl.pathname.startsWith('/project/')) {

    // Extract the user's primary email address from sessionClaims
    const userEmail = sessionClaims?.userEmail || '';  // Use the email from sessionClaims
    console.log('userEmail:', userEmail);
    const projectMiddlewareResponse = await handleProjectMiddleware(req, userEmail);
    if (projectMiddlewareResponse.status !== 200) {
      return projectMiddlewareResponse;
    }
  }
    // For users visiting /onboarding, don't try to redirect
    else if (userId && isOnboardingRoute(req)) {
      return NextResponse.next()
    }

    // If the user isn't signed in and the route is private, redirect to sign-in
    else if (!userId && !isPublicRoute(req)) {
      return redirectToSignIn({ returnBackUrl: req.url })
    }

    // Catch users who do not have `onboardingComplete: true` in their publicMetadata
    // Redirect them to the /onboarding route to complete onboarding
    else if (userId && !sessionClaims?.metadata?.onboardingComplete) {
      const onboardingUrl = new URL('/onboarding', req.url)
      return NextResponse.redirect(onboardingUrl)
    }

    // If the user is logged in and the route is protected, let them view.
    else if (userId && !isPublicRoute(req) || userId && isHomeRoute(req)) {
      return NextResponse.next()
    }

    else if (userId && isPublicRoute(req)) {
      const dashboardUrl = new URL('/dashboard', req.url)
      return NextResponse.redirect(dashboardUrl)
    }
  // }
  return NextResponse.next()
})

export const config = {
  matcher: [
    // Skip Next.js internals and all static files, unless found in search params
    '/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)',
    // Always run for API routes
    '/(api|trpc)(.*)',
    // Include project routes
    '/project/:path*',
  ],
}
