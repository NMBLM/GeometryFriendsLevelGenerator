using System.Collections;
using System.Collections.Generic;
using GeometryFriends.LevelGenerator;
using UnityEngine;
using Random = System.Random;

public class Generator : MonoBehaviour
{

    private int POPULATION_SIZE = 10;
    private Random random;

    private GeneticAlgorithm ga;
    
    
    // Start is called before the first frame update
    void Start()
    {
        
        random = new Random();
        
        ga = new GeneticAlgorithm(POPULATION_SIZE, random,FitnessFunction);
    }

    // Update is called once per frame
    void Update()
    {
        ga.NewGeneration();
        if (ga.bestLevel != null)
        {
            Debug.Log("Generation number: " + ga.generationNumber + "\ncurrent best = " +ga.bestFitness +"\n" + ga.bestLevel.Description() + "\n\n");
        }
        if (ga.bestFitness > .99)
        {
            Debug.Log("Best found");
            
            Debug.Log(ga.bestLevel.Description());
            
            this.enabled = false;
        }
        
    }



    public float FitnessFunction(int index)
    {
        ga.population[index].fitness = (float) random.NextDouble();
        return ga.population[index].fitness;
    }
}
