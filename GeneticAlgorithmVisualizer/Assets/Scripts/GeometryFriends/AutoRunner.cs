using System.Collections;
using System.Collections.Generic;
using System.Linq;
using GeneticSharp.Domain;
using GeneticSharp.Domain.Chromosomes;
using GeometryFriends.WithGS;
using UnityEngine;
namespace GeometryFriends
{
    public class AutoRunner : MonoBehaviour
    {
        [SerializeField] GameObject GAprefab;
        [SerializeField] ReachabilityViewer va;
        private int runAmount = 5;
    
        private int currentRun = 0;
    
        private GameObject currentGA = null;
    
        private GeneticAlgorithm ga = null;

        private bool takeScreenShot = false;

        private List<IChromosome> previousChromosomes;

        private bool showingTopTen = false;

        private int currentTopTen = 0;
        // Start is called before the first frame update
        void Start()
        {
            
        }
    
        // Update is called once per frame
        void Update()
        {
            if (!(currentRun >= runAmount))
            {
                if (currentGA == null)
                {
                    currentGA = Instantiate(GAprefab, this.transform);
                    ga = currentGA.GetComponent<SmallerLevelSampleController>().GA;
                    if (ga == null)
                    {
                        ga = currentGA.GetComponent<LevelSampleController>().GA;
                    }
        
                    if (ga == null)
                    {
                        Debug.Log("No proper Genetic Algorithm found");
                        currentRun = runAmount;
                    }
                }
        
                if (ga == null)
                {
                    if (currentGA == null)
                    {
                        return;
                    }
                    ga = currentGA.GetComponent<SmallerLevelSampleController>().GA;
                    if (ga == null)
                    {
                        ga = currentGA.GetComponent<LevelSampleController>().GA;
                    }
        
                    if (ga == null)
                    {
                        Debug.Log("No proper Genetic Algorithm found");
                        currentRun = runAmount;
                    }  
                }
                
                
                
                if (ga != null && ga.State == GeneticAlgorithmState.TerminationReached)
                {
                    previousChromosomes = ga.Population.CurrentGeneration.Chromosomes.OrderByDescending(c => c.Fitness.Value).ToList();
                    for (int i = 0; i < 10; i++)
                    {
                        InstrumentationManager.instance.WriteBestChromosome(previousChromosomes[i]); 
                    }
                    InstrumentationManager.instance.AddToDescription("Total Time: " + ga.TimeEvolving);
                    currentRun += 1;
                    if (currentRun < runAmount)
                    {
                        Destroy(currentGA); 
                    }
                    currentGA = null;
                    ga = null;
                    showingTopTen = true;
                    currentTopTen = 0;
                }
            }
            if (takeScreenShot)
            {
                InstrumentationManager.instance.Screenshot("Run" + currentRun + "_" + currentTopTen);
                takeScreenShot = false;
            }
            
            if (showingTopTen)
            {
                var tmp = previousChromosomes[currentTopTen];
                if (tmp.GetType() == typeof(LevelChromosome))
                {
                    var c = (LevelChromosome) tmp;
                    va.ViewBest(c);
                }
                else if (tmp.GetType() == typeof(SmallerLevelChromosome))
                {
                    var c = (SmallerLevelChromosome) tmp;
                    va.ViewBest(c);
                }
                currentTopTen++;
                takeScreenShot = true;
                if (currentTopTen >= 10)
                {
                    showingTopTen = false;
                }
            }

        }
    }
}