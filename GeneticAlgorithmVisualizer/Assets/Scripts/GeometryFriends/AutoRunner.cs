using System.Collections;
using System.Collections.Generic;
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
        private int runAmount = 10;
    
        private int currentRun = 0;
    
        private GameObject currentGA = null;
    
        private GeneticAlgorithm ga = null;
        // Start is called before the first frame update
        void Start()
        {
            
        }
    
        // Update is called once per frame
        void Update()
        {
            if (currentRun >= runAmount)
            {
                return;
            }
    
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
                InstrumentationManager.instance.WriteBestChromosome(ga.BestChromosome);
                if (ga.BestChromosome.GetType() == typeof(LevelChromosome))
                {
                    var c = (LevelChromosome) ga.BestChromosome;
                    va.ViewBest(c);
                }
                else if (ga.BestChromosome.GetType() == typeof(SmallerLevelChromosome))
                {
                    var c = (SmallerLevelChromosome) ga.BestChromosome;
                    va.ViewBest(c);
                }
                currentRun += 1;
                Destroy(currentGA);
                currentGA = null;
                ga = null;
            }
    
            
        }
    }
}