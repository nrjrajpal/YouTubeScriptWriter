import { NextResponse } from 'next/server';

export async function middleware(request: Request) {
  const url = new URL(request.url);
  const projectId = url.pathname.split('/')[3];

  if (url.pathname.startsWith('/project/') && projectId) {
    try {
      // Check if the project exists
      const checkProjectUrl = `${process.env.API_BASE_URL}/api/checkProject/${projectId}`;
      const checkProjectResponse = await fetch(checkProjectUrl);

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
      const getNextStageUrl = `${process.env.API_BASE_URL}/api/getNextStage/${projectId}`;
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

// Configuration to apply middleware only to /project routes
export const config = {
  matcher: ['/project/:path*'],
};
