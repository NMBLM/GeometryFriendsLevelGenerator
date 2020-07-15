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
    "11111001011100110000111111001011001100100101010100110001100011010000010010101011111100101011110101101111111001100001000010111000000101101100110000011110101100110111000100100100010110011011101110000001101010000101001110100001010101100111011100101010011001100011111011001000001001110110101111010000011101100010001101000000000010011011000011010100100111001101011110000111010001010001011110010101110000110000001000100111111111001101110010000100010001011011000101111110011101001011001111001100101001010100000100101010011011111000001011111100101111000110011001000001100011010001100001000101";
        
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
        //level = GATestWorld.LevelTwo();
        
        //level = GATestWorld.LevelSpecificationOneTest();
        //level = GATestWorld.LevelSpecificationTwoTest();
        //level = GATestWorld.LevelTest();

        level = (new SmallerLevelChromosome(lvlString)).GetLevelDNA();
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
        h = new AreaHeuristic(TestSpecifications.LevelTwo());
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
        h = new AreaHeuristic(TestSpecifications.LevelTwo());
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
