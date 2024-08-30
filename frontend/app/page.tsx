'use client';
import { useRouter } from "next/navigation";
import { BackpackIcon } from "@radix-ui/react-icons";
import Image from "next/image";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import Link from "next/link";

export default function Home() {
  const router = useRouter();
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm lg:flex">
        <Link
          href={"http://www.fomento.to.gov.br"}
          className="hover:cursor-pointer"
        >
          <Image
            className="relative dark:drop-shadow-[0_0_0.3rem_#ffffff70] dark:invert "
            src="/Logo Texto Colorido.png"
            alt="Next.js Logo"
            width={280}
            height={27}
            priority
          />
        </Link>
      </div>

      <div className="">
        <div className="mt-2 flex flex-wrap justify-around px-2 ">
          <Card
            onClick={() => router.push("/app/juridico")}
            className="hover:cursor-pointer w-60 items-center p-2 shadow-xl transition-transform hover:scale-105  hover:bg-accent"
          >
            <CardHeader className="flex max-w-xs flex-row justify-center space-y-0 pb-2">
              <CardTitle className="flex flex-col justify-center text-sm font-medium text-orange-500 ">
                <div className="text-2xl font-bold">Jurídico</div>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex flex-col items-center justify-center">
                <BackpackIcon width="24" height="24" />
                <p className="mt-2 text-xs text-muted-foreground">jurídico</p>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>

      <div className="mb-32 grid text-center lg:max-w-5xl lg:w-full lg:mb-0 lg:grid-cols-4 lg:text-left"></div>
    </main>
  );
}
