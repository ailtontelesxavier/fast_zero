import NextAuth from "next-auth";
import CredentialsProvider from "next-auth/providers/credentials";
import axios from "axios";
import api from "@/lib/api";
import { decodeJwt } from 'jose';

// These two values should be a bit less than actual token lifetimes
const BACKEND_ACCESS_TOKEN_LIFETIME = 60 * 60;            // 40 minutes
const BACKEND_REFRESH_TOKEN_LIFETIME = 1 * 24 * 60 * 60;  // 1 days

const getCurrentEpochTime = () => {
  return Math.floor(new Date().getTime() / 1000);
};

function getTimeElapsed(iat) {
  const currentUnixTime = Math.floor(new Date().getTime() / 1000); // Tempo atual em segundos
  const timeElapsed = currentUnixTime - iat; // Diferença entre o tempo atual e o iat fornecido
  const newIat = iat + timeElapsed; // Adiciona a diferença ao iat original para obter o novo iat

  return newIat;
};

export const dynamic = 'force-dynamic';

const SIGN_IN_HANDLERS = {
  "credentials": async (user, account, profile, email, credentials) => {
    return true;
  },
};
const SIGN_IN_PROVIDERS = Object.keys(SIGN_IN_HANDLERS);

const authOptions = {
  url: process.env.NEXTAUTH_URL || "http://localhost:3000",
  // No static secret used
  secret: process.env.NEXTAUTH_SECRET,
  session: {
    strategy: "jwt",
    updateAge: BACKEND_ACCESS_TOKEN_LIFETIME,
    maxAge: BACKEND_REFRESH_TOKEN_LIFETIME
  },

  providers: [
    CredentialsProvider({
      name: "Credentials",
      credentials: {
        domain: {
          label: "Domain",
          type: "text",
          placeholder: "FOMENTO",
          value: "FOMENTO",
        },
        username: { label: "Username", type: "text" },
        password: { label: "Password", type: "password" },
        client_secret: { label: "OTP", type: "text" }
      },
      async authorize(credentials, req) {
        try {
          const response = await axios({
            url: process.env.NEXTAUTH_BACKEND_URL + "/auth/token",
            method: "post",
            data: credentials,
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
          });
          const data = response.data;
          if (data) {
            data.forceNewToken = true;
            return data;
          }
        } catch (error) {
          console.error(error);
        }
        return null;
      },
    })
  ],
  callbacks: {
    async signIn({ user, account, profile, email, credentials }) {
      if (!SIGN_IN_PROVIDERS.includes(account.provider)) return false;
      return SIGN_IN_HANDLERS[account.provider](user, account, profile, email, credentials);
    },
    async jwt({ user, token, account }) {
      if (user && account) {
        let backendResponse = account.provider === "credentials" ? user : account.meta;

        token["access_token"] = backendResponse.access_token;
        token["refresh_token"] = backendResponse.refresh_token;

        const decoded = decodeJwt(backendResponse.access_token);
        //console.log(decoded)
        token['exp'] = decoded.exp;
        token['sub'] = decoded.sub;
        return token;
      }
      const valide = await verifyToken(token["access_token"])
      //if (!token.forceNewToken && getCurrentEpochTime() > token['exp']) {
      if (!valide) {
        //delete token.access_token;
        //signOut();
        return null;
      }
      
      //delete token.forceNewToken;
      return token;
    },
    async session({ token }) {
      return token;
    }
  },
  pages: {
    signIn: "/authentication",
  }
};

const handler = NextAuth(authOptions);
export { handler as GET, handler as POST };

async function verifyToken(access_token) {
  try {
    //console.log(access_token)
    const response = await axios({
      url: process.env.NEXTAUTH_BACKEND_URL + "/auth/verify-token",
      method: "get",
      headers: { "Authorization": `Bearer ${access_token}`,
        //"Content-Type": "application/x-www-form-urlencoded"
      },
    }).catch((error) => {
      //console.log(error)
      return false;
    });
    //console.log(response)
    if (response.status == 200) {
      return true
    }
    return false
  } catch (error) {
    console.log(error)
    return false
  }
  return false
}