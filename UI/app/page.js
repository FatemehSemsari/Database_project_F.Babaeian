import Image from "next/image";
import Hero from "@/components/layout/Hero";


export default function Home() {
  return (
    <div className="min-h-screen bg-[#122b4e]">
      <main className="bg-[#122a4c]">
        <Hero/>
      </main>
    </div>
  );
}
