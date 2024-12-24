export { }

declare global {
    interface CustomJwtSessionClaims {
        metadata: {
            onboardingComplete?: boolean
        },
        userEmail: string
    }
}