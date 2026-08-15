import Link from "next/link"

export default function UserProfileMenu(){
    return(
        <div className=" text-white w-4/12 h-auto p-5 bg-[#10243D]">
            <div>

            </div>
            <div className=" flex flex-col gap-3">
                <Link href={"/profile"} />
            </div>
        </div>
    )
}