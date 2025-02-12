'use server'

import { auth, clerkClient } from '@clerk/nextjs/server'

export const completeOnboarding = async (formData: FormData) => {
    const { userId } = await auth()

    if (!userId) {
        return { message: 'No Logged In User' }
    }

    const client = await clerkClient()

    try {
        const res = await client.users.updateUser(userId, {
            publicMetadata: {
                onboardingComplete: true,
                applicationName: formData.get('applicationName'),
                applicationType: formData.get('applicationType'),
            },
        })
        return { message: res.publicMetadata }
        // eslint-disable-next-line @typescript-eslint/no-unused-vars
    } catch (err) { 
        return { error: 'There was an error updating the user metadata.' }
    }
}