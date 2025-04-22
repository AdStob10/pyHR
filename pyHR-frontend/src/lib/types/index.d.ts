type TokenData = {
    access_token: string
    token_type: string
}

type UserData = {
    id: number,
    username: string,
    email: string | undefined
}

export type {TokenData, UserData}