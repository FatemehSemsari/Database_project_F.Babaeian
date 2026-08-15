import { mockFilters } from "@/data/mockData"
import { useRef } from "react"

export default function SearchFillter({searchHandler}){
    const datetoRef = useRef(null)
     const timetoRef = useRef(null)
     const datefromRef = useRef(null)
      const timefromRef = useRef(null)
    const sportRef = useRef(null)
    const cityRef = useRef(null)
    const venueRef = useRef(null)
    const nameRef = useRef(null)

    return(
        <div>
            <div className=" h-25 bg-blue-950 text-white  mt-25 flex flex-wrap flex-row-reverse justify-around p-2 items-center rounded-xl">
            <select ref={sportRef}>
               {
                mockFilters.teams.map((teams) =>{
                    return <option value={teams.id}>{teams.name}</option>
                })
               }
            </select>
            <select ref={sportRef}>
               {
                mockFilters.sports.map((sport) =>{
                    return <option value={sport.id}>{sport.name}</option>
                })
               }
            </select>
            <select ref={venueRef}>
                  {
                mockFilters.venues.map((venue) =>{
                    return <option value={venue.id}>{venue.name}</option>
                })
               }
            </select>
             <select ref={cityRef}>
                 {
                mockFilters.cities.map((city) =>{
                    return <option value={city.id}>{city.name}</option>
                })
               }
                
            </select>
            
            <div className="flex flex-col justify-center items-center">
                <div className="flex  gap-6 justify-around items-center">
                <input dir="rtl" className="border-b-2 rounded-md p-1 text-right" type="date" ref={datetoRef}></input>
                <span>:تا</span>
                <input  dir="rtl" className="border-b-2 rounded-md p-1 text-right" type="date" ref={datefromRef}></input>
                <span className="mr-8">:از تاریخ</span>
                </div>
                {/* <div className="mt-2 flex  gap-2 justify-around items-center">
                <input dir="rtl" className=" border-b-2 rounded-md p-1 text-right" type="time" ref={timetoRef}></input>
                <span className="mr-5">:تا</span>
                <input dir="rtl" className="border-b-2 rounded-md p-1 text-right" type="time" ref={timefromRef}></input>
                <span>:از ساعت</span>
                </div> */}
            </div>
            
            <button onClick={()=>searchHandler(sportRef.current.value, cityRef.current.value, venueRef.current.value, datetoRef.current.value, datefromRef.current.value, timetoRef.current.value, timefromRef.current.value,nameRef.current.value)} className=" text-black flex w-30 items-center justify-center bg-[#52D15C] p-3 rounded-lg">
            جستجو
            <svg className=" w-5 m-1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M12.323 13.383a5.5 5.5 0 1 1 1.06-1.06l2.897 2.897a.75.75 0 1 1-1.06 1.06l-2.897-2.897Zm.677-4.383a4 4 0 1 1-8 0 4 4 0 0 1 8 0Z"/></svg>
          </button>
         </div>
         
    
        </div>
       
    )
}