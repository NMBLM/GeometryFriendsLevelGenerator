using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using GeneticSharp.Domain.Chromosomes;
using UnityEngine;


namespace GeometryFriends
{
    public class InstrumentationManager: MonoBehaviour
    {
        #region Singleton

        public static InstrumentationManager instance;
        private String _filepath;
        private DirectoryInfo _dir;
        private void Awake() {
            instance = this;

            //_spottedPosition = new List<Tuple<GameObject, Vector3>>(); // Guard, PlayerSpotted Position
            //_caughtPosition = new List<Tuple<GameObject, Vector3>>(); // Guard, PlayerCaught Position
            //_openDoorDetected = new List<Tuple<GameObject, GameObject>>(); // door, guard
            //_nodeVistited = new List<Tuple<GameObject, GameObject>>(); // Node, guard
            //var dirName = "Gen_" ;
            var RunNumber = 0;
            using (StreamReader sr = new StreamReader(Directory.GetCurrentDirectory() + "\\GenData\\RunNumber.txt"))
            {
                string line = sr.ReadLine();
                if(line!=null)
                RunNumber = Int32.Parse(line);
            }

            RunNumber++;
            using (StreamWriter writer = new StreamWriter(Directory.GetCurrentDirectory() + "\\GenData\\RunNumber.txt"))
            {
                writer.Write(RunNumber);
            }
            using (StreamWriter writer = new StreamWriter(Directory.GetCurrentDirectory() + "\\GenData\\RunNumber.txt"))
            {
                writer.Write(RunNumber);
            }

            _dir = Directory.CreateDirectory(Directory.GetCurrentDirectory()+"\\GenData\\Run_" + RunNumber);
            _filepath =_dir.FullName + "\\data.txt";
            Debug.Log(_filepath);

        }

        #endregion

        public void WriteGenData(int GenNumber, IList<IChromosome> chromosomes)
        {
            var orderedChromosomes = chromosomes.OrderByDescending(c => c.Fitness.Value).ToList();
            String text = "Gen " + GenNumber + "\n";
            //Best
            text += orderedChromosomes[0].Fitness.Value+"\n";
            
            //Average
            double average = orderedChromosomes.Average(c => c.Fitness.Value);
            text += average + "\n";

            int bp = orderedChromosomes.Count / 4;
            double fq = 0;
            double sq = 0;
            double tq = 0;
            double lq = 0;
            for (int i = 0; i < orderedChromosomes.Count; i++)
            {
                if (i < bp)
                {
                    fq += orderedChromosomes[i].Fitness.Value;
                }else if (i < 2 * bp)
                {
                    sq += orderedChromosomes[i].Fitness.Value;

                }else if (i < 3 * bp)
                {
                    tq += orderedChromosomes[i].Fitness.Value;
                }
                else
                {
                    lq += orderedChromosomes[i].Fitness.Value;
                }
            }
            //Average First Quartil
            text += (fq / bp) + "\n";
            
            //Average Second Quartil
            text += (sq / bp) + "\n";

            //Average Third Quartil
            text += (tq / bp) + "\n";

            //Average Fourth Quartil
            text += (lq / bp) + "\n";

            using (StreamWriter sw = new StreamWriter(_filepath,true))
            {
                sw.Write(text);
            }

            using (StreamWriter sw = new StreamWriter(_dir.FullName + "\\chromosomes.txt",true))
            {
                sw.Write("Gen " + GenNumber + "\n");
                foreach (var c in orderedChromosomes)
                {
                    sw.Write(c.Fitness.Value + "\n");
                }
            }

            
        }
        
        
    }
}