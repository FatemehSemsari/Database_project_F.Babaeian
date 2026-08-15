"use client"
import { useRef } from "react"
export default function ModifyModal({modify , closeModal}){

    const timeRef=useRef()
    return(
         <div className=" wrapper fixed inset-0 z-[100] flex justify-center items-center">
        <div  onClick={closeModal} className="absolute min-h-screen inset-0 bg-black/80" />
         <div        onClick={(e) => e.stopPropagation()} className="flip-card__front">
                <div className="title">تمدید مهلت انقضا بلیط</div>
                <form className="flip-card__form" >
                  <input  className="flip-card__input" ref={timeRef} name="email" placeholder="مدت زمان تمدید" type="date" />
                  
                  <button onClick={()=>modify(timeRef.current.value)} className="flip-card__btn">تمدید</button>
                </form>
              </div> 
      </div>
    )
}