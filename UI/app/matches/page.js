import MatchCard from "@/components/layout/MatchCard";
import SearchFillter from "@/components/layout/SearchFillter";

export default function Matches(){
    return(
        <div className=" min-h-screen m-auto w-11/12">
            <SearchFillter></SearchFillter>
            <MatchCard></MatchCard>
        </div>
    );
}