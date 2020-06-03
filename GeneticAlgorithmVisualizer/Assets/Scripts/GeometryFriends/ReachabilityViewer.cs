using System;
using System.Collections;
using System.Collections.Generic;
using GeometryFriends;
using GeometryFriends.LevelGenerator;
using GeometryFriends.WithGS;
using UnityEngine;
using UnityEngine.UI;
using Random = System.Random;
public class ReachabilityViewer : MonoBehaviour
{

    [SerializeField] private Material unreachableMaterial;
    [SerializeField] private Material platformMaterial;
    [SerializeField] private Material rectangleReachMaterial;
    [SerializeField] private Material circleReachMaterial;
    [SerializeField] private Material cooperativeReachMaterial;
    [SerializeField] private Material bothReachMaterial;
    [SerializeField] private Material collectibleMaterial;
    [SerializeField] private GameObject gridBlockPrefab;
    [SerializeField] private float granularity = 16f;

    private String lvlString =
        "10101011110100011110110000100010001010101101000010010101011001001100110001111110110010101010000010010110000100001110001100100100000010001110111110110101001011111110110110111110110011110101100010000011010001111001101000111001000001110111111100001101000111001010010011100111010100111010111010100011111101111000011001001100111100001000010101101101101111100110110001101101001011011000010011011000001011011011000100111100000001011111101111011000100001110111100101000100000101111001000000100010110101110001101001111011010011000111101000001010100110101100001111011100010110110011001110110100000101001101101011000010001010111110011011110001011110011111110111011001011100111010111110111110000011100011110100011111110100111110000111110100110110110011110101000";
    
    public LevelDNA level;
    
    //public OldReachHeuristic h;
    public AreaHeuristic h;
    
    public Random random;

    public GAController GC;

    public LevelSampleController GS;
    public SmallerLevelSampleController SGS;
    // Start is called before the first frame update
    [SerializeField] private int currentN = 0;
    [SerializeField] private int toGen = 1;
    void Start()
    {
        /** /
        random = new Random();
        var chromosome = new LevelChromosome();
        Debug.Log(chromosome.ToString());
        level = chromosome.GetLevelDNA();
        //level = new LevelDNA(random, TmpFit, init: true);
        //level = new LevelDNA(random, TmpFit, init: false);
        
        Debug.Log("Level: " + level.Description());
        h = new OldReachHeuristic(blockSize:granularity);
        h.CalculateFitness(level);
        h.CellGridToBlockGrid();
        CreateGrid();
        
        //Debug.Log(level.Description());
        
        /** /
        //level = GATestWorld.LevelOne();
        level = GATestWorld.LevelTwo();
        
        //level = GATestWorld.LevelSpecificationOneTest();
        //level = GATestWorld.LevelSpecificationTwoTest();
        //level = GATestWorld.LevelTest();

        //level = (new LevelChromosome(lvlString)).GetLevelDNA();
        Debug.Log(level.Description());
        //h = new OldReachHeuristic(blockSize:granularity);
        h = new AreaHeuristic(TestSpecifications.LevelTwo());
        Debug.Log(h.CalculateFitness(level));
        //h.CellGridToBlockGrid();
        CreateGrid();
        
        /**/
        /** /
        Debug.Log(GATestWorld.LevelOne().DNAToChromosome());
        Debug.Log(GATestWorld.LevelOne().DNAToChromosome().GetLevelDNA().Description());
        Debug.Log(GATestWorld.LevelOne().Description());
        Debug.Log("-------------------------------------");
        Debug.Log(GATestWorld.LevelTwo().DNAToChromosome());
        Debug.Log(GATestWorld.LevelTwo().DNAToChromosome().GetLevelDNA().Description());
        Debug.Log(GATestWorld.LevelTwo().Description());
        /** /
        Debug.Log(GATestWorld.LevelOne().DNAToSmallChromosome());
        Debug.Log(GATestWorld.LevelOne().DNAToSmallChromosome().GetLevelDNA().Description());
        Debug.Log(GATestWorld.LevelOne().Description());
        Debug.Log("-------------------------------------");
        Debug.Log(GATestWorld.LevelTwo().DNAToSmallChromosome());
        Debug.Log(GATestWorld.LevelTwo().DNAToSmallChromosome().GetLevelDNA().Description());
        Debug.Log(GATestWorld.LevelTwo().Description());
        /**/
        //GC = new GAController();
    }

    // Update is called once per frame
    void Update()
    {
        /** /
        if (Input.GetKeyUp(KeyCode.R))
        {
            foreach (Transform child in transform)
            {
                if (child != this.transform)
                {
                    Destroy(child.gameObject);
                }
            }
            var chromosome = new LevelChromosome();
            Debug.Log(chromosome.ToString());
            level = chromosome.GetLevelDNA();
            //level = new LevelDNA(random, TmpFit, init: true);
            Debug.Log("Level: " + level.Description());
            //h = new OldReachHeuristic(blockSize:granularity);
            h = new AreaHeuristic(TestSpecifications.LevelOne());

            h.CalculateFitness(level);
            h.CellGridToBlockGrid();

            CreateGrid();
        
            //Debug.Log(level.Description());
        }
        /**/

        /** /
        if (Input.GetKeyUp(KeyCode.O))
        {
            currentN -= 1;
            if (currentN < 0) currentN = 0;
            GC.ShowNPopulation(currentN);
            Debug.Log("Viewing: " + currentN);
        }
        if (Input.GetKeyUp(KeyCode.P))
        {
            currentN += 1;
            
            if (!GC.ShowNPopulation(currentN)) currentN -= 1;
            Debug.Log("Viewing: " + currentN);
        }
        if (Input.GetKeyUp(KeyCode.N))
        {
            GC.NextGen(toGen+1);
        }
        /**/
        /** /
        if (Input.GetKeyUp(KeyCode.O))
        {
            if (GS == null)
            {
                var o = GameObject.Find("SampleController");
                GS = o.GetComponent<LevelSampleController>();
            }
            else
            {
                currentN -= 1;
                if (currentN < 0) currentN = 0;
                GS.ShowNPopulation(currentN);
                Debug.Log("Viewing: " + currentN);  
            }
            
        }
        if (Input.GetKeyUp(KeyCode.P))
        {
            if (GS == null)
            {
                var o = GameObject.Find("SampleController");
                GS = o.GetComponent<LevelSampleController>();
            }
            else
            {
                currentN += 1;
                if (!GS.ShowNPopulation(currentN)) currentN -= 1;
                Debug.Log("Viewing: " + currentN);   
            }
            
        }
        /**/
        /**/
        if (Input.GetKeyUp(KeyCode.O))
        {
            if (SGS == null)
            {
                var o = GameObject.Find("SmallSampleController");
                SGS = o.GetComponent<SmallerLevelSampleController>();
            }
            else
            {
                currentN -= 1;
                if (currentN < 0) currentN = 0;
                SGS.ShowNPopulation(currentN);
                Debug.Log("Viewing: " + currentN);  
            }
            
        }
        if (Input.GetKeyUp(KeyCode.P))
        {
            if (SGS == null)
            {
                var o = GameObject.Find("SmallSampleController");
                SGS = o.GetComponent<SmallerLevelSampleController>();
            }
            else
            {
                currentN += 1;
                if (!SGS.ShowNPopulation(currentN)) currentN -= 1;
                Debug.Log("Viewing: " + currentN);   
            }
            
        }
        /**/
    }

    public void ViewBest(LevelChromosome best)
    {
        foreach (Transform child in transform)
        {
            if (child != this.transform)
            {
                Destroy(child.gameObject);
            }
        }
        Debug.Log("Fitness : " + best.Fitness);
        level = best.GetLevelDNA();
        Debug.Log("Level: " + level.Description() + "\n" + best.ToString());
        h = new AreaHeuristic(TestSpecifications.LevelOne());
        //h = new OldReachHeuristic(blockSize:granularity);
        Debug.Log("recalculated fitness: " + h.CalculateFitness(level));
        CreateGrid();
    }
    
    public void ViewBest(SmallerLevelChromosome best)
    {
        foreach (Transform child in transform)
        {
            if (child != this.transform)
            {
                Destroy(child.gameObject);
            }
        }
        Debug.Log("Fitness : " + best.Fitness);
        level = best.GetLevelDNA();
        Debug.Log("Level: " + level.Description() + "\n" + best.ToString());
        h = new AreaHeuristic(TestSpecifications.LevelOne());
        //h = new OldReachHeuristic(blockSize:granularity);
        Debug.Log("recalculated fitness: " + h.CalculateFitness(level));
        CreateGrid();
    }
    public float TmpFit(int index)
    {
        return -1.0f;
    }

    public void CreateGrid()
    {
        for (int i = 0; i < h.xGridLen; i++)
        {
            for (int j = 0; j < h.yGridLen; j++)
            {
                var block = Instantiate(gridBlockPrefab, new Vector3(0.5f*i, -0.5f*j, 0), Quaternion.identity);
                block.transform.parent = this.gameObject.transform;
                var mat = block.GetComponent<Renderer>();
                switch (h.grid[i,j])
                {
                    case BlockType.Unreachable:
                        mat.material = unreachableMaterial;
                        break;
                    case BlockType.Platform:
                        mat.material = platformMaterial;
                        break;
                    case BlockType.RectangleCanReach:
                        mat.material = rectangleReachMaterial;
                        break;
                    case BlockType.CircleCanReach:
                        mat.material = circleReachMaterial;
                        mat.material.color = (float)(h.cellGrid[i,j].jumpStrength+16)/40 * Color.yellow;
                        break;
                    case BlockType.CooperativeCanReach:
                        mat.material = cooperativeReachMaterial;
                        mat.material.color = (float)(h.cellGrid[i,j].jumpStrength+16)/40 * Color.cyan;
                        break;
                    case BlockType.BothCanReach:
                        mat.material = bothReachMaterial;
                        break;
                }
            }
        }
        
        int x = (int) ((level.rectangleSpawn.position.X - 40)/ h.blockSize)  + 2;
        int y = (int) ((level.rectangleSpawn.position.Y - 40)/ h.blockSize)  + 2;
        for (int i = 0; i < 3; i++)
        {
            for (int j = 0; j < 3; j++)
            {
                var recSpawnBlock = 
                    Instantiate(gridBlockPrefab, new Vector3(0.5f*x + 0.5f *i, -0.5f*y - 0.5f *j, -0.5f), Quaternion.identity);
                recSpawnBlock.transform.parent = this.gameObject.transform;
                var recSpawnMat = recSpawnBlock.GetComponent<Renderer>();
                recSpawnMat.material = rectangleReachMaterial;
            }
        }
        
        x = (int) ((level.circleSpawn.position.X - 40)/ h.blockSize)  + 2;
        y = (int) ((level.circleSpawn.position.Y - 40)/ h.blockSize)  + 2;
        for (int i = 0; i < 80/h.blockSize; i++)
        {
            for (int j = 0; j < 80/h.blockSize; j++)
            {
                var circleSpawnBlock =
                    Instantiate(gridBlockPrefab, new Vector3(0.5f*x + 0.5f *i, -0.5f*y - 0.5f *j, -0.5f), Quaternion.identity);
                circleSpawnBlock.transform.parent = this.gameObject.transform;
                var circleSpawnMat = circleSpawnBlock.GetComponent<Renderer>();
                circleSpawnMat.material = circleReachMaterial;
            }
        }

        foreach (var col in level.collectibles)
        {
            x = (int) ((col.position.X - 40)/ h.blockSize)  + 2;
            y = (int) ((col.position.Y - 40)/ h.blockSize)  + 2;
            var collectibleBlock =
                Instantiate(gridBlockPrefab, new Vector3(0.5f*x, -0.5f*y, -0.5f), Quaternion.identity);
            collectibleBlock.transform.parent = this.gameObject.transform;
            var circleSpawnMat = collectibleBlock.GetComponent<Renderer>();
            circleSpawnMat.material = collectibleMaterial;
        }
    }
}
